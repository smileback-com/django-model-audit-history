# django-model-audit-history

Provides an `AuditHistory` model field to store a chronological record of changes to a model (“audit history”) on the model. The historical record is stored in a designated JSON field, so no additional database tables are required.

Supports Django 1.11 (and possibly Django 2.x in the future) and PostgreSQL database backends.

## CI

[![Build Status](https://travis-ci.org/nexto/django-model-audit-history.svg?branch=master)](https://travis-ci.org/nexto/django-model-audit-history)

## Usage

The basic principles are as follows:

1. To enable this for a model, you make two changes:

   * add an `AuditHistoryField` named `history` to the model
   * add the `AuditHistoryMixin` to the model class
   * add your model to admin site `admin.site.register(model, AuditHistoryAdmin)`

2. Then, instead of calling regular `save()` on the model after changing it, call `save_with_audit_record()` instead (passing in some meta data you want saved alongside, e.g. the `event` that caused the change, the `user` triggering it and some `payload` usually the set of modified fields.

3. The history will appear in human-readable form in the admin.

That’s pretty much all there is to it.

## Limitations

Changes made to the model in the admin right now unfortunately do not contribute to the audit record.

## Testapp setup and first steps

1. Install Postgres locally (e.g. 10.x)
2. Create local database `audithistory`, owned by user `dev`
3. Create a virtualenv and activate: `virtualenv venv`, then `source venv/bin/activate`
4. Install dependencies into virtualenv: `pip install --requirement requirements.txt`
5. Run `manage.py migrate`
6. Run `manage.py createsuperuser`
7. Run `manage.py runserver`
8. Create new model on http://localhost:8000/admin/test_app/blogpost/
9. Edit model via http://localhost:8000/edit/1/
10. Reload admin page and inspect history record

## Run tests in local environment:

* Run `manage.py test` (Ensure that user dev has rights to db creation `alter user dev createdb;`)
