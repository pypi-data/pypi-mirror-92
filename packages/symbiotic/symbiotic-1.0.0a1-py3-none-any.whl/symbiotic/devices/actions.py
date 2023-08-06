import atexit
import functools
import logging
import secrets
from abc import ABC
from contextlib import contextmanager
from typing import Callable, List

from ..core import _event_bus, _scheduler


class Action(object):

    bus = _event_bus
    scheduler = _scheduler

    def __init__(self, func: Callable = None, *args, **kwargs):
        if not func and (args or kwargs):
            raise TypeError('Parameters set, but no function passed.')

        self.name = kwargs.pop('name', secrets.token_hex(16))
        self.func = functools.partial(func, *args, **kwargs) if func else None
        atexit.register(self.unregister)
        super().__init__()

    def __eq__(self, other: 'Action'):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))

    def __call__(self):
        if self.func is None:
            err = f'The action {self.name} does not have a callable function.'
            raise AttributeError(err)

        return self.func()

    def do(self, func: Callable, *args, **kwargs) -> 'Action':
        self.func = functools.partial(func, *args, **kwargs)
        return self

    def unregister(self) -> None:
        """ Override to unregister the action from its handler. """
        pass


class EventedAction(Action):

    event: str

    def __init__(self, on: str, **kwargs):
        super().__init__(**kwargs)
        self.event = on
        self.bus.add_event(self, self.event)
        logging.debug(f'{self.event} registered on bus')

    def unregister(self) -> None:
        """ Removes the action from the bus. """
        # Dirty hack to make the bus remove events:
        # the bus method does comparison by using instance.__name__ == instance
        # but this fails because class instances of Action don't have __name__
        # Implementing __name__ wouldn't work as we override __eq__, so it
        # would try to compare an instance of Action to a string.
        # This could be solved in a better way, but the lazy one take less time.
        self.__name__ = self
        self.bus.remove_event(self, self.event)
        logging.debug(f'removed {self.event} from bus')


class ScheduledAction(Action):

    def __init__(self, func: Callable = None, *args, **kwargs):
        super().__init__(func, *args, **kwargs)
        self.job = None

    def every(self, interval: int = 1):
        self.job = self.scheduler.every(interval).tag(self.name)
        return self.job

    def register(self):
        if not self.job:
            err = f"Cannot schedule '{self.name}': no schedule specified"
            raise AttributeError(err)

        self.job.do(self)
        logging.debug(f'{self.name} added to the schedule')

    def unregister(self) -> bool:
        self.scheduler.cancel_job(self.job)
        logging.debug(f'{self.name} removed from the schedule')
        return True


class ActionScheduler(object):

    def __init__(self, func: Callable = None, **kwargs):
        self.name = kwargs.pop('name', None)
        self.func = func
        self.kwargs = kwargs
        self.actions = []
        atexit.register(self.clear)
        super().__init__()

    def add(self, func: Callable = None, *args, **kwargs):
        if func is not None:
            # action specified
            action = ScheduledAction(func, *args, **{**self.kwargs, **kwargs})
        else:
            if self.func is None:
                raise TypeError('Cannot schedule an empty action.')
            action = ScheduledAction(
                self.func, *args, **{**self.kwargs, **kwargs})
        self.actions.append(action)
        return action

    def _finalize(self):
        for action in self.actions:
            action.register()

    def clear(self):
        # mutate existing list by adding back only actions if failed to unregister
        self.actions[:] = [act for act in self.actions if not act.unregister()]


class Actionable(ABC):

    actions: List[Action]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = []

    def event(self, name: str, **kwargs) -> Action:
        action = EventedAction(name)
        self.actions.append(action)
        return action

    @contextmanager
    def schedule(self, job: Callable = None, **kwargs) -> ActionScheduler:
        """ Registers the action with the scheduler.

        Using contextmanager allows to yield an instance of ActionScheduler
        and to set the scheduled job's job (i.e. this action) from within
        this method, which gives us more control.

        Example:
            >>> with device.schedule(device.action) as schedule:
            >>>     schedule.add().every().day.at('08.30')
            >>>     schedule.add().every(5).days.at('11.30')
        """
        scheduler = ActionScheduler(job, **kwargs)
        yield scheduler
        scheduler._finalize()
