# SPDX-License-Identifier: MIT
"""
Daemon Handler - Rueckwaertskompatibilitaets-Wrapper
=====================================================

DEPRECATED: Dieses Modul ist ein thin wrapper fuer hub.scheduler.
Bitte kuenftig "from hub.scheduler import SchedulerHandler" verwenden.

Dieser Wrapper bleibt dauerhaft fuer Rueckwaertskompatibilitaet erhalten.
"""

# Re-Export aus scheduler (neuer Name)
from .scheduler import SchedulerHandler, SchedulerHandler as DaemonHandler

__all__ = ["DaemonHandler", "SchedulerHandler"]
