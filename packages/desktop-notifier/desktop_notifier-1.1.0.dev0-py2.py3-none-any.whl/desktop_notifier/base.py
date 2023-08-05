# -*- coding: utf-8 -*-
"""
This module defines base classes for desktop notifications. All platform implementations
must inherit from :class:`DesktopNotifierBase`.
"""

# system imports
from enum import Enum
from typing import Optional, Dict, Callable, Union


class NotificationLevel(Enum):
    """Enumeration of notification levels

    The interpretation and visuals will depend on the platform.

    :cvar Critical: For critical errors.
    :cvar Normal: Default platform notification level.
    :cvar Low: Low priority notification.
    """

    Critical = "critical"
    Normal = "normal"
    Low = "low"


class Notification:
    """A desktop notification

    :param title: Notification title.
    :param message: Notification message.
    :param urgency: Notification level: low, normal or critical. This is ignored by some
        implementations.
    :param icon: Path to an icon to use for the notification, typically the app icon.
        This is ignored by some implementations, e.g., on macOS where the icon of the
        app bundle is always used.
    :param action: Handler to call when the notification is clicked. This is ignored by
        some implementations.
    :param buttons: A dictionary with button names to show in the notification and
        handler to call when the respective button is clicked. This is ignored by some
        implementations.

    :ivar identifier: An identifier which gets assigned to the notification after it is
        sent. This may be a str or int, depending on the type of identifier used by the
        platform.
    """

    identifier: Union[str, int, None]

    def __init__(
        self,
        title: str,
        message: str,
        urgency: NotificationLevel = NotificationLevel.Normal,
        icon: Optional[str] = None,
        action: Optional[Callable] = None,
        buttons: Optional[Dict[str, Callable]] = None,
    ) -> None:

        self.title = title
        self.message = message
        self.urgency = urgency
        self.icon = icon
        self.action = action
        self.buttons = buttons or dict()
        self.identifier = None

    def __repr__(self):
        return f"<{self.__class__.__name__}(title='{self.title}', message='{self.message}')>"


class DesktopNotifierBase:
    """Base class for desktop notifier implementations

    Notification levels CRITICAL, NORMAL and LOW may be used by some implementations to
    determine how a notification is displayed.

    :param app_name: Name to identify the application in the notification center.
    :param notification_limit: Maximum number of notifications to keep in the system's
        notification center.
    """

    app_name: str
    notification_limit: int
    current_notifications: Dict[int, Notification]

    def __init__(self, app_name: str = "", notification_limit: int = 5) -> None:
        self.app_name = app_name
        self.notification_limit = notification_limit
        self.current_notifications = dict()
        self._current_nid = 0

    def send(self, notification: Notification) -> None:
        """
        Sends a desktop notification. Some arguments may be ignored, depending on the
        implementation.

        :param notification: Notification to send.
        """
        pass

    def _next_nid(self) -> int:
        self._current_nid += 1
        self._current_nid %= self.notification_limit
        return self._current_nid
