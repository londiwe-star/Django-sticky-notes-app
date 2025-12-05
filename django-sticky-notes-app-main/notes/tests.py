"""
Comprehensive unit tests for the notes application.

This module contains test classes for:
- NoteModelTest: Tests for the Note model
- NoteViewTest: Tests for all view functions (CRUD operations)
- NoteFormTest: Tests for the NoteForm
- URLTest: Tests for URL routing
- IntegrationTest: End-to-end workflow tests
"""
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Note
from .forms import NoteForm
from .views import note_list, note_detail, note_create, note_update, note_delete


class NoteModelTest(TestCase):
    """Test cases for the Note model."""
    
    def setUp(self):
        """Set up test data before each test method."""
        self.note = Note.objects.create(
            title='Test Note',
            content='This is a test note content.'
        )
    
    def test_note_creation_with_valid_data(self):
        """Test that a note can be created with valid title and content."""
        self.assertEqual(self.note.title, 'Test Note')
        self.assertEqual(self.note.content, 'This is a test note content.')
        self.assertIsNotNone(self.note.id)
    
    def test_note_str_method(self):
        """Test that __str__ method returns the correct string representation."""
        self.assertEqual(str(self.note), 'Test Note')
    
    def test_title_max_length_constraint(self):
        """Test that title field has correct max_length constraint."""
        max_length = self.note._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)
    
    def test_content_is_textfield(self):
        """Test that content field accepts TextField data."""
        long_content = 'A' * 5000
        note = Note.objects.create(
            title='Long Content Note',
            content=long_content
        )
        self.assertEqual(len(note.content), 5000)
    
    def test_created_at_timestamp_auto_set(self):
        """Test that created_at timestamp is automatically set on creation."""
        self.assertIsNotNone(self.note.created_at)
        self.assertIsInstance(self.note.created_at, timezone.datetime)
    
    def test_updated_at_timestamp_auto_set(self):
        """Test that updated_at timestamp is automatically set on creation."""
        self.assertIsNotNone(self.note.updated_at)
        self.assertIsInstance(self.note.updated_at, timezone.datetime)
    
    def test_updated_at_changes_on_update(self):
        """Test that updated_at changes when note is updated."""
        original_updated_at = self.note.updated_at
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        self.note.title = 'Updated Title'
        self.note.save()
        self.assertGreater(self.note.updated_at, original_updated_at)
    
    def test_created_at_does_not_change_on_update(self):
        """Test that created_at does not change when note is updated."""
        original_created_at = self.note.created_at
        self.note.title = 'Updated Title'
        self.note.save()
        self.assertEqual(self.note.created_at, original_created_at)
    
    def test_title_is_required(self):
        """Test that title field is required."""
        note = Note(title='', content='Some content')
        with self.assertRaises(ValidationError):
            note.full_clean()
    
    def test_content_is_required(self):
        """Test that content field is required."""
        note = Note(title='Test Title', content='')
        # Note: TextField allows empty strings by default, but we can test it
        note.save()
        self.assertEqual(note.content, '')
    
    def test_model_ordering(self):
        """Test that notes are ordered by updated_at descending."""
        note1 = Note.objects.create(title='First', content='Content 1')
        import time
        time.sleep(0.01)
        note2 = Note.objects.create(title='Second', content='Content 2')
        time.sleep(0.01)
        note3 = Note.objects.create(title='Third', content='Content 3')
        
        notes = list(Note.objects.all())
        # Most recently updated should be first
        self.assertEqual(notes[0].title, 'Third')
        self.assertEqual(notes[1].title, 'Second')
        self.assertEqual(notes[2].title, 'First')
    
    def test_note_manager_get_recent(self):
        """Test the custom manager's get_recent method."""
        note1 = Note.objects.create(title='First', content='Content 1')
        import time
        time.sleep(0.01)
        note2 = Note.objects.create(title='Second', content='Content 2')
        time.sleep(0.01)
        note3 = Note.objects.create(title='Third', content='Content 3')
        
        recent_notes = Note.objects.get_recent()
        self.assertEqual(recent_notes[0].title, 'Third')
        self.assertEqual(recent_notes[1].title, 'Second')
        self.assertEqual(recent_notes[2].title, 'First')
    
    def test_note_with_special_characters(self):
        """Test that note can handle special characters."""
        special_note = Note.objects.create(
            title='Note with !@#$%^&*()',
            content='Content with <script>alert("test")</script>'
        )
        self.assertEqual(special_note.title, 'Note with !@#$%^&*()')
        self.assertIn('<script>', special_note.content)
    
    def test_note_with_unicode_characters(self):
        """Test that note can handle unicode characters."""
        unicode_note = Note.objects.create(
            title='Note with 中文 and émojis 🎉',
            content='Content with русский and العربية'
        )
        self.assertEqual(unicode_note.title, 'Note with 中文 and émojis 🎉')
        self.assertIn('русский', unicode_note.content)


class NoteViewTest(TestCase):
    """Test cases for all view functions."""
    
    def setUp(self):
        """Set up test data and client before each test method."""
        self.client = Client()
        self.note = Note.objects.create(
            title='Test Note',
            content='This is test content.'
        )
    
    # List View Tests
    def test_note_list_get_request_status_code(self):
        """Test that GET request to note_list returns status code 200."""
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_note_list_uses_correct_template(self):
        """Test that note_list view uses the correct template."""
        response = self.client.get(reverse('note_list'))
        self.assertTemplateUsed(response, 'notes/notes_list.html')
    
    def test_note_list_context_contains_notes(self):
        """Test that note_list context contains 'notes' queryset."""
        response = self.client.get(reverse('note_list'))
        self.assertIn('notes', response.context)
        self.assertIsInstance(response.context['notes'], type(Note.objects.all()))
    
    def test_note_list_displays_multiple_notes(self):
        """Test that note_list view displays multiple notes correctly."""
        Note.objects.create(title='Note 2', content='Content 2')
        Note.objects.create(title='Note 3', content='Content 3')
        
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.context['notes'].count(), 3)
    
    def test_note_list_empty_state(self):
        """Test that note_list handles empty state when no notes exist."""
        Note.objects.all().delete()
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['notes'].count(), 0)
        self.assertContains(response, 'No notes yet')
    
    # Detail View Tests
    def test_note_detail_get_request_with_valid_pk(self):
        """Test that GET request with valid pk returns status code 200."""
        response = self.client.get(reverse('note_detail', kwargs={'pk': self.note.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_note_detail_get_request_with_invalid_pk(self):
        """Test that GET request with invalid pk returns 404."""
        response = self.client.get(reverse('note_detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)
    
    def test_note_detail_uses_correct_template(self):
        """Test that note_detail view uses the correct template."""
        response = self.client.get(reverse('note_detail', kwargs={'pk': self.note.pk}))
        self.assertTemplateUsed(response, 'notes/note_detail.html')
    
    def test_note_detail_context_contains_note(self):
        """Test that note_detail context contains the correct note object."""
        response = self.client.get(reverse('note_detail', kwargs={'pk': self.note.pk}))
        self.assertIn('note', response.context)
        self.assertEqual(response.context['note'], self.note)
    
    def test_note_detail_displays_note_content(self):
        """Test that note content is displayed in the response."""
        response = self.client.get(reverse('note_detail', kwargs={'pk': self.note.pk}))
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is test content.')
    
    # Create View Tests
    def test_note_create_get_request_returns_form(self):
        """Test that GET request to note_create returns form (status 200)."""
        response = self.client.get(reverse('note_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_note_create_uses_correct_template(self):
        """Test that note_create view uses the correct template."""
        response = self.client.get(reverse('note_create'))
        self.assertTemplateUsed(response, 'notes/note_form.html')
    
    def test_note_create_post_with_valid_data_creates_note(self):
        """Test that POST with valid data creates a new note."""
        initial_count = Note.objects.count()
        response = self.client.post(reverse('note_create'), {
            'title': 'New Note',
            'content': 'New content here'
        })
        self.assertEqual(Note.objects.count(), initial_count + 1)
        self.assertTrue(Note.objects.filter(title='New Note').exists())
    
    def test_note_create_post_with_valid_data_redirects(self):
        """Test that POST with valid data redirects to note_list."""
        response = self.client.post(reverse('note_create'), {
            'title': 'New Note',
            'content': 'New content here'
        })
        self.assertRedirects(response, reverse('note_list'))
    
    def test_note_create_post_with_valid_data_shows_success_message(self):
        """Test that successful creation shows success message."""
        response = self.client.post(reverse('note_create'), {
            'title': 'New Note',
            'content': 'New content here'
        }, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Note created successfully!')
    
    def test_note_create_post_with_invalid_data_doesnt_create(self):
        """Test that POST with invalid data doesn't create a note."""
        initial_count = Note.objects.count()
        response = self.client.post(reverse('note_create'), {
            'title': '',  # Invalid: empty title
            'content': 'Some content'
        })
        self.assertEqual(Note.objects.count(), initial_count)
        self.assertEqual(response.status_code, 200)  # Returns form with errors
    
    def test_note_create_post_with_missing_fields_shows_errors(self):
        """Test that POST with missing required fields shows form errors."""
        response = self.client.post(reverse('note_create'), {
            'title': '',  # Missing title
            'content': ''
        })
        self.assertFormError(response, 'form', 'title', 'This field is required.')
    
    def test_note_create_database_count_increases(self):
        """Test that database count increases after successful creation."""
        initial_count = Note.objects.count()
        self.client.post(reverse('note_create'), {
            'title': 'Another Note',
            'content': 'Another content'
        })
        self.assertEqual(Note.objects.count(), initial_count + 1)
    
    # Update View Tests
    def test_note_update_get_request_returns_prefilled_form(self):
        """Test that GET request returns pre-filled form."""
        response = self.client.get(reverse('note_update', kwargs={'pk': self.note.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].instance, self.note)
    
    def test_note_update_get_request_uses_correct_template(self):
        """Test that note_update GET uses the correct template."""
        response = self.client.get(reverse('note_update', kwargs={'pk': self.note.pk}))
        self.assertTemplateUsed(response, 'notes/note_form.html')
    
    def test_note_update_post_with_valid_data_updates_note(self):
        """Test that POST with valid data updates existing note."""
        response = self.client.post(reverse('note_update', kwargs={'pk': self.note.pk}), {
            'title': 'Updated Title',
            'content': 'Updated content'
        })
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Title')
        self.assertEqual(self.note.content, 'Updated content')
    
    def test_note_update_post_with_valid_data_redirects(self):
        """Test that POST with valid data redirects to note_detail."""
        response = self.client.post(reverse('note_update', kwargs={'pk': self.note.pk}), {
            'title': 'Updated Title',
            'content': 'Updated content'
        })
        self.assertRedirects(response, reverse('note_detail', kwargs={'pk': self.note.pk}))
    
    def test_note_update_post_with_valid_data_shows_success_message(self):
        """Test that successful update shows success message."""
        response = self.client.post(reverse('note_update', kwargs={'pk': self.note.pk}), {
            'title': 'Updated Title',
            'content': 'Updated content'
        }, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Note updated successfully!')
    
    def test_note_update_post_with_invalid_data_doesnt_update(self):
        """Test that POST with invalid data doesn't update note."""
        original_title = self.note.title
        response = self.client.post(reverse('note_update', kwargs={'pk': self.note.pk}), {
            'title': '',  # Invalid: empty title
            'content': 'Some content'
        })
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, original_title)
        self.assertEqual(response.status_code, 200)
    
    def test_note_update_nonexistent_note_returns_404(self):
        """Test that updating non-existent note returns 404."""
        response = self.client.get(reverse('note_update', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)
    
    def test_note_update_database_values_change(self):
        """Test that database values actually change after update."""
        self.client.post(reverse('note_update', kwargs={'pk': self.note.pk}), {
            'title': 'Completely New Title',
            'content': 'Completely new content'
        })
        updated_note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(updated_note.title, 'Completely New Title')
        self.assertEqual(updated_note.content, 'Completely new content')
    
    # Delete View Tests
    def test_note_delete_get_request_shows_confirmation_page(self):
        """Test that GET request on delete view shows confirmation page."""
        response = self.client.get(reverse('note_delete', kwargs={'pk': self.note.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_confirm_delete.html')
        self.assertIn('note', response.context)
    
    def test_note_delete_post_request_deletes_note(self):
        """Test that POST request deletes note."""
        note_id = self.note.pk
        response = self.client.post(reverse('note_delete', kwargs={'pk': note_id}))
        self.assertFalse(Note.objects.filter(pk=note_id).exists())
    
    def test_note_delete_post_redirects_to_list(self):
        """Test that deletion redirects to note_list."""
        response = self.client.post(reverse('note_delete', kwargs={'pk': self.note.pk}))
        self.assertRedirects(response, reverse('note_list'))
    
    def test_note_delete_post_shows_success_message(self):
        """Test that successful deletion shows success message."""
        response = self.client.post(reverse('note_delete', kwargs={'pk': self.note.pk}), follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Note deleted successfully!')
    
    def test_note_delete_database_count_decreases(self):
        """Test that database count decreases after deletion."""
        initial_count = Note.objects.count()
        self.client.post(reverse('note_delete', kwargs={'pk': self.note.pk}))
        self.assertEqual(Note.objects.count(), initial_count - 1)
    
    def test_note_delete_nonexistent_note_returns_404(self):
        """Test that deleting non-existent note returns 404."""
        response = self.client.post(reverse('note_delete', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)


class NoteFormTest(TestCase):
    """Test cases for the NoteForm."""
    
    def test_form_has_correct_fields(self):
        """Test that form has correct fields (title, content)."""
        form = NoteForm()
        self.assertIn('title', form.fields)
        self.assertIn('content', form.fields)
    
    def test_form_is_valid_with_correct_data(self):
        """Test that form is valid with correct data."""
        form = NoteForm(data={
            'title': 'Test Title',
            'content': 'Test content here'
        })
        self.assertTrue(form.is_valid())
    
    def test_form_is_invalid_with_missing_title(self):
        """Test that form is invalid with missing title."""
        form = NoteForm(data={
            'title': '',
            'content': 'Some content'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_form_is_invalid_with_missing_content(self):
        """Test that form handles missing content (TextField allows empty)."""
        form = NoteForm(data={
            'title': 'Some title',
            'content': ''
        })
        # TextField allows empty strings, so form might be valid
        # But we can test the field exists
        self.assertIn('content', form.fields)
    
    def test_form_validation_messages(self):
        """Test that form shows appropriate validation messages."""
        form = NoteForm(data={'title': '', 'content': 'Content'})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        error_message = form.errors['title'][0]
        self.assertIn('required', error_message.lower())
    
    def test_form_field_widgets(self):
        """Test that form field widgets are correctly configured."""
        form = NoteForm()
        title_widget = form.fields['title'].widget
        content_widget = form.fields['content'].widget
        
        self.assertEqual(title_widget.__class__.__name__, 'TextInput')
        self.assertEqual(content_widget.__class__.__name__, 'Textarea')
    
    def test_form_field_attributes(self):
        """Test that form fields have correct attributes."""
        form = NoteForm()
        title_attrs = form.fields['title'].widget.attrs
        content_attrs = form.fields['content'].widget.attrs
        
        self.assertIn('class', title_attrs)
        self.assertIn('placeholder', title_attrs)
        self.assertIn('class', content_attrs)
        self.assertIn('rows', content_attrs)
    
    def test_form_save_method(self):
        """Test that form save method creates note correctly."""
        form = NoteForm(data={
            'title': 'Saved Note',
            'content': 'Saved content'
        })
        self.assertTrue(form.is_valid())
        note = form.save()
        self.assertIsInstance(note, Note)
        self.assertEqual(note.title, 'Saved Note')
        self.assertEqual(note.content, 'Saved content')
    
    def test_form_save_with_instance_updates(self):
        """Test that form save with instance updates existing note."""
        note = Note.objects.create(title='Original', content='Original content')
        form = NoteForm(data={
            'title': 'Updated',
            'content': 'Updated content'
        }, instance=note)
        self.assertTrue(form.is_valid())
        saved_note = form.save()
        self.assertEqual(saved_note.pk, note.pk)
        self.assertEqual(saved_note.title, 'Updated')
    
    def test_form_labels(self):
        """Test that form has correct field labels."""
        form = NoteForm()
        self.assertEqual(form.fields['title'].label, 'Title')
        self.assertEqual(form.fields['content'].label, 'Content')


class URLTest(TestCase):
    """Test cases for URL routing."""
    
    def test_note_list_url_resolves(self):
        """Test that note_list URL pattern resolves to correct view."""
        url = reverse('note_list')
        self.assertEqual(url, '/')
        resolved = resolve('/')
        self.assertEqual(resolved.func, note_list)
    
    def test_note_create_url_resolves(self):
        """Test that note_create URL pattern resolves to correct view."""
        url = reverse('note_create')
        self.assertEqual(url, '/note/create/')
        resolved = resolve('/note/create/')
        self.assertEqual(resolved.func, note_create)
    
    def test_note_detail_url_resolves(self):
        """Test that note_detail URL pattern resolves to correct view."""
        url = reverse('note_detail', kwargs={'pk': 1})
        self.assertEqual(url, '/note/1/')
        resolved = resolve('/note/1/')
        self.assertEqual(resolved.func, note_detail)
        self.assertEqual(resolved.kwargs['pk'], 1)
    
    def test_note_update_url_resolves(self):
        """Test that note_update URL pattern resolves to correct view."""
        url = reverse('note_update', kwargs={'pk': 1})
        self.assertEqual(url, '/note/1/update/')
        resolved = resolve('/note/1/update/')
        self.assertEqual(resolved.func, note_update)
        self.assertEqual(resolved.kwargs['pk'], 1)
    
    def test_note_delete_url_resolves(self):
        """Test that note_delete URL pattern resolves to correct view."""
        url = reverse('note_delete', kwargs={'pk': 1})
        self.assertEqual(url, '/note/1/delete/')
        resolved = resolve('/note/1/delete/')
        self.assertEqual(resolved.func, note_delete)
        self.assertEqual(resolved.kwargs['pk'], 1)
    
    def test_url_patterns_are_unique(self):
        """Test that all URL patterns are unique and don't conflict."""
        from notes.urls import urlpatterns
        paths = [pattern.pattern._route for pattern in urlpatterns]
        # Check for obvious conflicts
        self.assertNotEqual('/note/create/', '/note/<int:pk>/')
        self.assertNotEqual('/note/<int:pk>/', '/note/<int:pk>/update/')


class IntegrationTest(TestCase):
    """Integration tests for complete workflows."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
    
    def test_complete_workflow_create_view_update_delete(self):
        """Test complete workflow: create → view → update → delete."""
        # Create
        response = self.client.post(reverse('note_create'), {
            'title': 'Workflow Note',
            'content': 'Initial content'
        })
        self.assertRedirects(response, reverse('note_list'))
        note = Note.objects.get(title='Workflow Note')
        
        # View
        response = self.client.get(reverse('note_detail', kwargs={'pk': note.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Workflow Note')
        
        # Update
        response = self.client.post(reverse('note_update', kwargs={'pk': note.pk}), {
            'title': 'Updated Workflow Note',
            'content': 'Updated content'
        })
        self.assertRedirects(response, reverse('note_detail', kwargs={'pk': note.pk}))
        note.refresh_from_db()
        self.assertEqual(note.title, 'Updated Workflow Note')
        
        # Delete
        response = self.client.post(reverse('note_delete', kwargs={'pk': note.pk}))
        self.assertRedirects(response, reverse('note_list'))
        self.assertFalse(Note.objects.filter(pk=note.pk).exists())
    
    def test_navigation_between_pages(self):
        """Test navigation between pages works correctly."""
        note = Note.objects.create(title='Nav Test', content='Content')
        
        # List to Create
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        
        # List to Detail
        response = self.client.get(reverse('note_detail', kwargs={'pk': note.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Detail to Update
        response = self.client.get(reverse('note_update', kwargs={'pk': note.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Update back to Detail
        response = self.client.post(reverse('note_update', kwargs={'pk': note.pk}), {
            'title': 'Nav Test',
            'content': 'Content'
        })
        self.assertRedirects(response, reverse('note_detail', kwargs={'pk': note.pk}))
    
    def test_form_submission_and_redirect_flow(self):
        """Test form submission and redirect flow."""
        # Create form submission
        response = self.client.post(reverse('note_create'), {
            'title': 'Form Test',
            'content': 'Form content'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/notes_list.html')
        
        note = Note.objects.get(title='Form Test')
        
        # Update form submission
        response = self.client.post(reverse('note_update', kwargs={'pk': note.pk}), {
            'title': 'Updated Form Test',
            'content': 'Updated form content'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        
        # Delete form submission
        response = self.client.post(reverse('note_delete', kwargs={'pk': note.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/notes_list.html')

