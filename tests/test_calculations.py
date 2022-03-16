import pytest
from app.calculation import add, subtract, multiply, divide, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount();

@pytest.fixture
def bank_account():
    return BankAccount(200)


@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (7,1,8),
    (12,4,16)
])


def test_add(num1, num2, expected):
    print("testing add function") 
    assert add(num1, num2) == expected

def test_subtract():
    print("testing subtract function") 
    assert subtract(5,3) == 2

def test_multiply():
    print("testing multiply function") 
    assert multiply(5,3) == 15

def test_divide():
    print("testing multiply function") 
    assert divide(15,3) == 5


def test_bank_set_initial_amount(bank_account):
    print("Creating empty bank account")
    assert bank_account.balance == 200

def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    print("Testing my bank account")
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(5)
    assert bank_account.balance == 195

def test_deposit(bank_account):
    # bank_account = BankAccount(200)
    bank_account.deposit(5)
    assert bank_account.balance == 205

def test_collect_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 220

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200,100,100),
    (258,10,248),
    (2,1,1)
])

def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(5000)