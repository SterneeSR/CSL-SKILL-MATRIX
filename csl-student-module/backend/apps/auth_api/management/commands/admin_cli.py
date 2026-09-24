import sys
from django.core.management.base import BaseCommand
from django.db.models import ProtectedError
from django.contrib.auth import get_user_model

from apps.skills.cli import SkillManagementCLI
from apps.courses.cli import CourseManagementCLI

User = get_user_model()


def _make_output_pipe_safe():
    """Keep CLI output alive when piped or redirected on Windows.

    Windows pipes default to cp1252, which cannot encode characters used in
    CLI output such as '✓' or the box-drawing tree characters. Replacing
    unencodable characters with '?' prevents a UnicodeEncodeError crash;
    interactive console output is unaffected.
    """
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(errors="replace")
            except (OSError, ValueError):
                pass


class Command(BaseCommand):
    help = "Run the interactive CSL Student Module Admin CLI."

    def handle(self, *args, **options):
        _make_output_pipe_safe()
        # ``input`` resolves at call time, so tests can script it by patching
        # builtins.input; real terminal use gets normal stdin input.
        self.input_fn = input
        self.stdout.write("Starting CSL Student Module Admin CLI...\n")
        try:
            self.main_menu()
        except (KeyboardInterrupt, EOFError):
            self.stdout.write("\nExiting Admin CLI. Goodbye!")
            sys.exit(0)

    def get_pending_count(self):
        return User.objects.filter(
            role=User.Role.STUDENT,
            status=User.AccountStatus.PENDING,
        ).count()

    def main_menu(self):
        while True:
            pending_count = self.get_pending_count()
            self.stdout.write("\n========================================")
            self.stdout.write("       CSL STUDENT MODULE ADMIN")
            self.stdout.write("========================================\n")
            self.stdout.write(f"1. Pending Users ({pending_count})")
            self.stdout.write("2. User Management")
            self.stdout.write("3. Skill Management")
            self.stdout.write("4. Course Management")
            self.stdout.write("5. Exit\n")

            choice = self.input_fn("Select option: ").strip()

            if choice == "1":
                self.pending_users_menu()
            elif choice == "2":
                self.user_management_menu()
            elif choice == "3":
                SkillManagementCLI(self, input_fn=self.input_fn).main_menu()
            elif choice == "4":
                CourseManagementCLI(self, input_fn=self.input_fn).main_menu()
            elif choice == "5":
                self.stdout.write("Exiting Admin CLI. Goodbye!")
                break
            else:
                self.stdout.write(self.style.WARNING("Invalid option. Please choose 1, 2, 3, 4, or 5."))

    def pending_users_menu(self):
        while True:
            pending_users = list(
                User.objects.filter(
                    role=User.Role.STUDENT,
                    status=User.AccountStatus.PENDING,
                ).order_by("created_at")
            )

            self.stdout.write("\nPENDING USERS\n")
            if not pending_users:
                self.stdout.write("No pending registration requests.\n")
                self.stdout.write("B. Back")
                choice = self.input_fn("\nSelect option: ").strip().lower()
                if choice == "b" or choice == "":
                    break
                else:
                    self.stdout.write(self.style.WARNING("Invalid option."))
                    continue

            self.stdout.write("-" * 40)
            for idx, user in enumerate(pending_users, start=1):
                name = user.first_name or "(not set)"
                reg_time = (
                    user.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if user.created_at
                    else "N/A"
                )
                self.stdout.write(f"{idx}. {user.email}")
                self.stdout.write(f"   Name: {name}")
                self.stdout.write(f"   Registered: {reg_time}")
                self.stdout.write("-" * 40)

            self.stdout.write("B. Back\n")
            selection = self.input_fn("Select user number (or B to go back): ").strip()

            if selection.lower() == "b":
                break

            if not selection.isdigit():
                self.stdout.write(self.style.WARNING("Please enter a valid number or 'B'."))
                continue

            user_idx = int(selection)
            if 1 <= user_idx <= len(pending_users):
                selected_user = pending_users[user_idx - 1]
                self.process_pending_user(selected_user)
            else:
                self.stdout.write(self.style.WARNING("Selection out of range."))

    def process_pending_user(self, user):
        # Refresh from database to ensure up-to-date status
        try:
            user.refresh_from_db()
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING("User no longer exists."))
            return

        if user.status != User.AccountStatus.PENDING:
            self.stdout.write(
                self.style.WARNING(f"User {user.email} is no longer PENDING (currently: {user.status}).")
            )
            return

        while True:
            self.stdout.write(f"\nSelected Student: {user.email} ({user.first_name or 'N/A'})")
            self.stdout.write("1. Approve")
            self.stdout.write("2. Decline")
            self.stdout.write("3. Back\n")

            choice = self.input_fn("Select option: ").strip()

            if choice == "1":
                user.status = User.AccountStatus.ACTIVE
                user.save(update_fields=["status", "updated_at"])
                self.stdout.write(self.style.SUCCESS("✓ Student approved successfully."))
                break
            elif choice == "2":
                user.status = User.AccountStatus.REJECTED
                user.save(update_fields=["status", "updated_at"])
                self.stdout.write(self.style.SUCCESS("✓ Student request declined."))
                break
            elif choice == "3":
                break
            else:
                self.stdout.write(self.style.WARNING("Invalid option. Please choose 1, 2, or 3."))

    def user_management_menu(self):
        while True:
            self.stdout.write("\nUSER MANAGEMENT\n")
            self.stdout.write("1. View Users")
            self.stdout.write("2. Delete User")
            self.stdout.write("3. Back\n")

            choice = self.input_fn("Select option: ").strip()

            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.delete_user()
            elif choice == "3":
                break
            else:
                self.stdout.write(self.style.WARNING("Invalid option. Please choose 1, 2, or 3."))

    def view_users(self):
        users = list(User.objects.all().order_by("created_at"))
        self.stdout.write("\nALL USERS\n")
        if not users:
            self.stdout.write("No users found in database.\n")
            return

        self.stdout.write("-" * 65)
        for idx, user in enumerate(users, start=1):
            name = user.first_name or "(not set)"
            created_str = (
                user.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if user.created_at
                else "N/A"
            )
            self.stdout.write(
                f"{idx}. {user.email}\n"
                f"   Name: {name}\n"
                f"   Role: {user.role}\n"
                f"   Status: {user.status}\n"
                f"   Created: {created_str}"
            )
            self.stdout.write("-" * 65)

        self.input_fn("\nPress Enter to return to User Management...")

    def delete_user(self):
        users = list(User.objects.all().order_by("created_at"))
        self.stdout.write("\nDELETE USER\n")
        if not users:
            self.stdout.write("No users available to delete.\n")
            return

        self.stdout.write("-" * 65)
        for idx, user in enumerate(users, start=1):
            name = user.first_name or "(not set)"
            self.stdout.write(f"{idx}. {user.email} (Role: {user.role}, Status: {user.status}, Name: {name})")
        self.stdout.write("-" * 65)
        self.stdout.write("B. Back\n")

        selection = self.input_fn("Select user number to delete (or B to cancel): ").strip()
        if selection.lower() == "b":
            return

        if not selection.isdigit():
            self.stdout.write(self.style.WARNING("Please enter a valid number or 'B'."))
            return

        user_idx = int(selection)
        if 1 <= user_idx <= len(users):
            selected_user = users[user_idx - 1]
            confirm = self.input_fn(
                f"Are you sure you want to delete this user ({selected_user.email})? (y/n): "
            ).strip().lower()

            if confirm == "y":
                try:
                    email = selected_user.email
                    selected_user.delete()
                    self.stdout.write(self.style.SUCCESS(f"✓ User {email} deleted successfully."))
                except ProtectedError as pe:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Cannot delete user {selected_user.email}: this user is referenced by protected records ({pe})."
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error deleting user {selected_user.email}: {e}")
                    )
            else:
                self.stdout.write("Deletion cancelled.")
        else:
            self.stdout.write(self.style.WARNING("Selection out of range."))
