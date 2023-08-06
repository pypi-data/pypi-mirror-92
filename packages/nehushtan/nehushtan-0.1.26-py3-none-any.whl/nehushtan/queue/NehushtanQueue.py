import os
import time
from multiprocessing import Pool

from nehushtan.queue.NehushtanQueueDelegate import NehushtanQueueDelegate
from nehushtan.queue.NehushtanQueueTask import NehushtanQueueTask
from nehushtan.queue.situation.NoNextTaskSituation import NoNextTaskSituation


class NehushtanQueue:
    def __init__(self, delegate: NehushtanQueueDelegate):
        self.delegate: NehushtanQueueDelegate = delegate
        self.current_workers = {}

    def get_logger(self):
        return self.delegate.logger

    def get_pool_capacity(self) -> int:
        """
        How many processes could run in the same time.
        Decided by the delegate
        """
        return self.delegate.read_config_of_delegate((NehushtanQueueDelegate.CONFIG_KEY_POOL_CAPACITY,), 1)

    def loop(self):
        self.delegate.when_loop_starts()

        with Pool(processes=self.get_pool_capacity()) as pool:
            while True:
                # Check existed workers' status before generate new workers
                self._refresh_count_of_current_workers()

                self.delegate.read_latest_command()

                # Check Command
                if self.delegate.should_terminate():
                    if self.delegate.should_wait_for_all_workers_before_terminating():
                        # wait for all worker processes done
                        self._refresh_count_of_current_workers(wait_till_less_than=1)
                        pass
                    break

                # Compare Pool Size and Capacity
                current_pool_size = len(self.current_workers.items())
                if current_pool_size >= self.get_pool_capacity():
                    self.delegate.when_pool_is_full()
                    if self.delegate.should_wait_when_pool_is_full():
                        # wait for any worker process done
                        self._refresh_count_of_current_workers(wait_till_less_than=self.get_pool_capacity())
                        pass
                    continue

                if not self.delegate.is_runnable():
                    self.delegate.when_loop_should_not_run()
                    continue

                try:
                    task = self.delegate.check_next_task()

                    if task.is_exclusive():
                        # now daemon should wait for the other tasks to be over
                        self._refresh_count_of_current_workers(wait_till_less_than=1)
                        pass

                    if not task.before_execute():
                        self.delegate.when_task_not_executable(task)
                        continue

                    task_async_process = pool.apply_async(
                        NehushtanQueue.embedded_task_execute,
                        args=(task, self.delegate)
                    )

                    self.current_workers[task.get_task_reference()] = task_async_process
                    self.delegate.when_worker_process_created(task.get_task_reference(), task_async_process.__str__())

                except NoNextTaskSituation:
                    self.delegate.when_no_task_to_do()
                    continue
                except Exception as loop_once_error:
                    self.delegate.when_loop_reports_error(loop_once_error.__str__())

        self.delegate.when_loop_terminates()

    def _refresh_count_of_current_workers(self, wait_till_less_than=0) -> int:
        if len(self.current_workers.items()) > 0:
            delete_keys = []
            for mapped_task_id, mapped_task_async_result in self.current_workers.items():
                try:
                    self.get_logger().debug('Checking Task Async Status', {'task_id': mapped_task_id})
                    if mapped_task_async_result.ready():
                        result = mapped_task_async_result.get(1)
                        if mapped_task_async_result.successful():
                            self.get_logger().info(
                                'Task Finished Successfully',
                                {"task_id": mapped_task_id, 'return': result}
                            )
                        else:
                            self.get_logger().warning(
                                'Task Finished Unsuccessfully',
                                {"task_id": mapped_task_id, 'return': result}
                            )
                        delete_keys.append(mapped_task_id)
                        self.delegate.when_worker_process_confirmed_dead(mapped_task_id, result)
                        # self.beat('whenChildProcessConfirmedDead',f'For Task {mapped_task_id}')
                except Exception as checking_async_exception:
                    self.get_logger().exception('Exception in checking async tasks', checking_async_exception)

            for delete_key in delete_keys:
                del self.current_workers[delete_key]
                self.get_logger().debug('remove removable finished tasks', {'task_id': delete_key})

        x = len(self.current_workers.items())
        if wait_till_less_than <= 0:
            # no need to wait, return
            return x
        else:
            if x < wait_till_less_than:
                # pool space is enough now
                return x
            else:
                # wait for processes to die
                self.get_logger().debug(f'Waiting for pool space. Now {x} out of {self.get_pool_capacity()} running.')
                time.sleep(2)
                return self._refresh_count_of_current_workers(wait_till_less_than=wait_till_less_than)

    @staticmethod
    def embedded_task_execute(embedded_task: NehushtanQueueTask, delegate: NehushtanQueueDelegate):
        """
        This works in WORKER
        """
        delegate.when_to_execute_task(embedded_task, os.getpid())
        try:
            embedded_task.execute()
        except Exception as e:
            delegate.when_task_raised_exception(embedded_task, e)
        delegate.when_task_executed(embedded_task, os.getpid())
