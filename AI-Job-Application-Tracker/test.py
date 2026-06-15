from services.application_service import add_application, get_all_applications


# Add a test application
add_application(
    "Google",
    "Software Engineer Intern",
    "Applied",
    "2026-06-14",
    "Referral applied via LinkedIn"
)

# Fetch all applications
apps = get_all_applications()

print(apps)