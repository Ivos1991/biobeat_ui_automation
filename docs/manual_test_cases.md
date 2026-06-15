# BioBeat Manual Test Cases

| # | Case | Steps | Expected Result |
|---|------|-------|-----------------|
| 1 | Login with valid credentials | Open login page, enter valid username and password, submit | User is authenticated and reaches the application shell |
| 2 | Navigate to Patient Admission | Log in, open Patients area, select Patient Admission | Patient Admission form is displayed with required fields visible |
| 3 | Happy path admission with required fields only | Open Patient Admission, enter unique Patient ID and valid Device ID, submit | Admission is accepted and success feedback is shown |
| 4 | Happy path admission with all optional fields | Open Patient Admission, populate all available fields, submit | Admission is accepted and optional data is persisted |
| 5 | Missing Patient ID | Leave Patient ID empty, enter valid Device ID, submit | Submission is blocked and Patient ID validation is shown |
| 6 | Missing Device ID | Enter Patient ID, leave Device ID empty, submit | Submission is blocked and Device ID validation is shown |
| 7 | Invalid Patient ID format | Enter unsupported Patient ID values such as special characters or overly long values, submit | UI displays format validation or blocks submission |
| 8 | Invalid Device ID format | Enter unsupported Device ID value, submit | UI displays validation or rejection for the Device ID |
| 9 | Device not assigned to client | Log in with current client user, submit a device known to belong elsewhere | UI rejects the device with a distinct client-assignment message |
| 10 | Device in wrong state | Submit a device ID in an ineligible state | UI rejects the device with a state-specific message distinct from format errors |
| 11 | Duplicate Patient ID in same department with active session | Use a Patient ID that already exists in the same department and currently has a relevant session state, submit | UI shows the expected duplicate or session-state handling for same-department reuse |
| 12 | Same Patient ID in different department | Create or locate same Patient ID in another department, then submit in current department | Behavior follows department scoping rules and does not incorrectly block the admission |
| 13 | Gender at Birth selection behavior | Open optional fields, choose each available gender option, submit | Selection is accepted and retained correctly |
| 14 | Date of Birth boundary coverage | Test future date, very old date, leap date, and minimum supported date | UI enforces valid date rules and accepts valid boundaries |
| 15 | Weight numeric validation | Enter alphabetic, negative, decimal, and very large weight values | Invalid values are blocked and valid numeric values are accepted |
| 16 | Height numeric validation | Enter alphabetic, negative, decimal, and very large height values | Invalid values are blocked and valid numeric values are accepted |
| 17 | Additional Notes boundaries and special characters | Enter max-length text, multiline text, punctuation, and symbols in Additional Notes | Supported characters are preserved and unsupported input is handled cleanly |
| 18 | Reset and Cancel behavior | Populate form, trigger Reset or Cancel, observe resulting state | Form is cleared or user is navigated away according to product behavior without partial submission |
| 19 | Back navigation behavior | Enter partial data, use Back control or browser back, return to form | Navigation behavior is consistent and data retention or discard matches product rules |
| 20 | Submission error handling | Trigger backend or network failure during submission | User receives actionable error feedback and no silent failure occurs |
