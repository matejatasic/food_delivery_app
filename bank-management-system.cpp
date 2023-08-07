#include <iostream>
#include <string>
#include <memory>
#include "repositories/transaction-repository.h"
#include "services/validation-service.h"
#include "services/bank-service.h"

using namespace std;

const int VALIDATION_VALID = 0;
const int VALIDATION_INVALID_NAME = 1;
const int VALIDATION_INVALID_PIN = 2;
const int VALIDATION_DATABASE_NOT_EXISTS_ERROR = 3;
const int VALIDATION_TABLE_NOT_EXISTS_ERROR = 4;
const int VALIDATION_DEFAULT_DATABASE_ERROR = 5;

int main()
{
    string name;
    string pin;

    cout << "\n\n----------------------\n";
    cout << "BANK MANAGEMENT SYSTEM";
    cout << "\n----------------------\n\n";

    cout << "Type in your name: ";
    cin >> name;
    cout << "Type in your pin: ";
    cin >> pin;
    cout << "\n";

    hash<string> string_hash;
    int hashed_pin = string_hash(pin);

    shared_ptr<Account> account = make_shared<Account>();
    shared_ptr<AccountRepository> account_repository = make_shared<AccountRepository>(account);

    ValidationService validation_service(account_repository);
    validation_service.validate_credentials(name, to_string(hashed_pin));

    if (validation_service.get_error_message().length() > 0) {
        cout << validation_service.get_error_message() << endl;

        return 1;
    }

    shared_ptr<TransactionRepository> transaction_repository = make_shared<TransactionRepository>();
    account = validation_service.get_account();
    shared_ptr<Transaction> transaction = make_shared<Transaction>();

    BankService bank_service(account_repository, transaction_repository, account, transaction);
    bank_service.run_app();

    return 0;
}