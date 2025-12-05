# Manual Testing Checklist for Sticky Notes Application

## 1. User Interface Testing

### Layout and Design

- [ ] Header displays correctly on all pages
- [ ] Footer displays correctly on all pages
- [ ] Navigation links are visible and properly styled
- [ ] CSS styling is applied correctly across all pages
- [ ] Responsive design works on mobile (if applicable)
- [ ] Forms are properly aligned and styled
- [ ] Buttons have hover effects
- [ ] Color scheme is consistent

### Template Rendering

- [ ] Base template extends correctly to all pages
- [ ] All static files (CSS) load without errors
- [ ] No broken images or missing resources
- [ ] Page titles are descriptive and correct

## 2. Functionality Testing

### Create Note

- [ ] "Create Note" or "Add Note" button is visible
- [ ] Clicking button navigates to create form
- [ ] Form displays title and content fields
- [ ] Submit button is present and clickable
- [ ] Submitting valid data creates note successfully
- [ ] Success message displays (if implemented)
- [ ] Redirects to appropriate page after creation
- [ ] New note appears in note list

### Read/View Notes

- [ ] Note list page displays all notes
- [ ] Each note shows title and content preview
- [ ] Clicking note title/link navigates to detail page
- [ ] Detail page shows full note content
- [ ] Created/updated timestamps display correctly (if implemented)
- [ ] "Back to list" link works correctly

### Update Note

- [ ] "Edit" button is visible on note detail page
- [ ] Clicking edit navigates to update form
- [ ] Form pre-populates with existing note data
- [ ] Changing data and submitting updates note
- [ ] Updated note shows new content
- [ ] Redirects appropriately after update

### Delete Note

- [ ] "Delete" button is visible on note detail page
- [ ] Confirmation prompt appears (if implemented)
- [ ] Confirming deletion removes note
- [ ] Note no longer appears in list
- [ ] Redirects to list page after deletion

## 3. Form Validation Testing

### Required Fields

- [ ] Submitting empty form shows validation errors
- [ ] Error messages are clear and helpful
- [ ] Missing title shows appropriate error
- [ ] Missing content shows appropriate error

### Edge Cases

- [ ] Very long title (200+ characters) is handled
- [ ] Very long content (5000+ characters) is handled
- [ ] Special characters in title (!@#$%^&*)
- [ ] Special characters in content
- [ ] HTML tags in input are escaped/sanitized
- [ ] Line breaks in content are preserved
- [ ] Unicode characters work correctly

## 4. Navigation Testing

- [ ] All internal links work correctly
- [ ] Breadcrumbs work (if implemented)
- [ ] Browser back button works as expected
- [ ] Direct URL access works for all pages
- [ ] 404 page displays for invalid URLs

## 5. Error Handling

- [ ] Accessing non-existent note ID shows 404
- [ ] Appropriate error messages for database errors
- [ ] Form errors display clearly
- [ ] Server errors don't expose sensitive information

## 6. Database Operations

- [ ] Create operation persists data correctly
- [ ] Read operation retrieves correct data
- [ ] Update operation modifies existing data
- [ ] Delete operation removes data permanently
- [ ] Data integrity is maintained

## 7. Admin Interface (if applicable)

- [ ] Admin login works
- [ ] Notes model appears in admin
- [ ] Can create notes through admin
- [ ] Can edit notes through admin
- [ ] Can delete notes through admin

## 8. Browser Compatibility (if time permits)

- [ ] Works in Chrome/Edge
- [ ] Works in Firefox
- [ ] Works in Safari

## Bugs Found During Manual Testing

[Document any bugs found here with:

- Description
- Steps to reproduce
- Expected vs actual behavior
- Severity (Critical/High/Medium/Low)]

## Testing Completed By

- Name: [Your Name]
- Date: [Date]
- Django Version: 4.2.0
- Python Version: 3.8+

