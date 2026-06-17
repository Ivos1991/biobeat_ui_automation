# BioBeat Manual Test Cases

| # | Case | Steps | Expected Result |
|---|------|-------|-----------------|
| 1 | Login with valid credentials | Open the login page, enter valid username and password, submit | User is authenticated and reaches Session Management |
| 2 | Navigate to Patient Admission | Log in, open Patients area, select Patient Admission | Patient Admission form is displayed with the core fields visible |
| 3 | Navigate to Patient Lookup | Log in, open Patients area, select Patient Lookup | Patient Lookup search input and table are visible |
| 4 | Happy path admission | Open Patient Admission, enter a unique Patient ID, valid available Device ID, and valid required live fields, submit and confirm with the same Patient ID | Admission succeeds and the new session is visible in Session Management |
| 5 | Happy path admission with valid Date of Birth | Open Patient Admission, enter valid required live fields plus a valid Date of Birth, submit and confirm with the same Patient ID | Admission succeeds and the new session is visible in Session Management |
| 6 | Cleanup and Remove Session flow | Create a valid admission, open Session Management, open Remove Session, confirm with the same Patient ID, remove the session | Remove button enables only for the exact Patient ID and the session disappears from Session Management |
| 7 | Missing Patient ID | Leave Patient ID empty, enter valid remaining data, submit | Submission is blocked and `Patient ID is required` is shown |
| 8 | Missing Device ID | Enter Patient ID, leave Device ID empty, submit | Submission is blocked and `Device ID is required` is shown |
| 9 | Device ID shorter than minimum length | Enter a Device ID shorter than 4 digits and submit | Submission is blocked and `Device ID must be at least 4 characters` is shown |
| 10 | Device already assigned to another active session | Create a valid session with an available device, return to Patient Admission, try to use the same Device ID for a different patient, submit and confirm | Submission is blocked, `Device is in use.` is shown, and the user remains on Patient Admission |
| 11 | Device not activated or does not exist | Enter a known invalid or inactive Device ID and submit and confirm | Submission is blocked, `Device is not activated or does not exist.` is shown, and the user remains on Patient Admission |
| 12 | Invalid First Name format | Enter numeric content in First Name and submit | Submission is blocked and `First name can not include special characters or numbers` is shown |
| 13 | Invalid Last Name format | Enter numeric content in Last Name and submit | Submission is blocked and `Last name can not include special characters or numbers` is shown |
| 14 | Weight below supported minimum | Enter weight `0` in kilograms and submit | Submission is blocked and `Weight must be between 10-250 kg` is shown |
| 15 | Weight above supported maximum | Enter weight `1000` in kilograms and submit | Submission is blocked and `Weight must be between 10-250 kg` is shown |
| 16 | Height below supported minimum | Enter height `0` in centimeters and submit | Submission is blocked and `Height must be between 30-242 cm` is shown |
| 17 | Height above supported maximum | Enter height `300` in centimeters and submit | Submission is blocked and `Height must be between 30-242 cm` is shown |
| 18 | Missing Referring Physician | Fill the rest of the live-required fields, leave Referring Physician empty, submit | Submission is blocked and `Referring physician is required` is shown |
| 19 | Invalid Patient ID characters | Enter unsupported Patient ID characters such as `@@@` and submit | Submission is blocked and `Patient ID can only contain numbers and letters` is shown |
| 20 | Future Date of Birth | Enter a future date and submit | Submission is blocked and `Date of birth cannot be in the future` is shown |
| 21 | Unsupported Additional Notes characters | Enter unsupported special characters such as `< > $ ^` in Additional Notes and submit | Submission is blocked and `Special characters < > $ ^ are not allowed.` is shown |
| 22 | Confirmation popup exact Patient ID behavior | Fill valid form data, open the admission confirmation popup, try empty and wrong Patient ID values, then the exact Patient ID | Confirm stays disabled for empty and wrong values and enables only for the exact Patient ID |
| 23 | Exit popup cancel and leave behavior | Type a Patient ID, open the exit popup, cancel it, then open it again and leave | Cancel preserves the form data, Leave returns the user to Session Management |
| 24 | Female Gender at Birth selection behavior | Fill valid form data with Female selected, submit | The confirmation popup opens normally, proving the Female option is accepted |
