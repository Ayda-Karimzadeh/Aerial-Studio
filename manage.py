#!/usr/bin/env python
"""نقطه ورود مدیریتی جنگو برای پروژه Aerial Studio."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django یافت نشد. مطمئن شوید که نصب شده و در PYTHONPATH قرار دارد."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
