# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Copyright (c) 2026 Lukas Geiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict
from datetime import datetime, date

class ItemCategory(Enum):
    """Kategorien von Items"""
    ROUTINE = "routine"      # Routine mit Schritten
    TASK = "task"            # Einmalige Aufgabe
    APPOINTMENT = "appointment"  # Zeitgebundener Termin

class IntervalType(Enum):
    """Wiederholungs-Typen"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class TimeSlot(Enum):
    """Tageszeiten"""
    MORNING = "morning"      # 06:00 - 12:00
    NOON = "noon"            # 12:00 - 17:00
    EVENING = "evening"      # 17:00 - 22:00
    NIGHT = "night"          # 22:00 - 06:00

@dataclass
class Step:
    """Ein Schritt innerhalb einer Routine"""
    id: str
    item_id: str
    title: str
    description: Optional[str] = None
    image_path: Optional[str] = None
    position: int = 0
    level: int = 1
    duration_minutes: Optional[int] = None
    parent_step_id: Optional[str] = None
    
    # Runtime (nicht in DB)
    is_completed: bool = False
    completed_at: Optional[datetime] = None

@dataclass
class Item:
    """Ein Item (Routine, Aufgabe oder Termin)"""
    id: str
    title: str
    category: ItemCategory = ItemCategory.TASK
    description: Optional[str] = None
    
    # Zeit
    has_time: bool = False
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    
    # Wiederholung
    has_recurrence: bool = False
    interval_type: Optional[IntervalType] = None
    interval_value: int = 1
    weekdays: Optional[List[int]] = None
    
    # Status
    is_active: bool = False
    is_template: bool = False
    template_id: Optional[str] = None
    
    # Darstellung
    color_code: str = "blue"
    icon: Optional[str] = None
    sort_order: int = 0
    
    # Meta
    person_id: int = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Runtime
    steps: List[Step] = field(default_factory=list)

@dataclass
class ItemInstance:
    """Eine tägliche Instanz eines Items"""
    id: str
    item_id: str
    due_date: date
    instance_number: int = 1
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    
    # Runtime
    item: Optional[Item] = None
    steps: List[Step] = field(default_factory=list)
    progress: float = 0.0

@dataclass
class TodayBoardItem:
    """Ein Item auf dem Heute-Board"""
    id: str
    instance: ItemInstance
    sort_order: int
    time_slot: Optional[TimeSlot] = None
