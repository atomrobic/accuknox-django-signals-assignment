# AccuKnox Django Trainee Assignment

## Setup
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations signals_demo
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Project structure
- `signals_demo/models.py`: sender and receiver-log models
- `signals_demo/signals.py`: signal receiver
- `signals_demo/tests.py`: executable proofs for Questions 1–3
- `custom_classes/rectangle.py`: iterable Rectangle class
- `custom_classes/tests.py`: Rectangle tests

## Django Signals — conclusions

1. **Synchronous:** `post_save.send()` calls receivers directly. The receiver finishes before `save()` returns.
2. **Same thread:** the receiver runs in the thread that caused the signal, unless custom code explicitly moves work to another thread/process.
3. **Same transaction:** not unconditionally. If the caller wraps the save in `transaction.atomic()`, receiver database writes use the same connection/transaction and roll back with it. Under normal autocommit outside an explicit atomic block, the receiver's database write can commit independently.

Run `python manage.py test` to execute the demonstrations.
