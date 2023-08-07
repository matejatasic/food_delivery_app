#include <iostream>
#include <cmath>
#include "bank-service.h"
#include "../errors/errors.h"

using namespace std;

BankService::BankService(
    shared_ptr<AccountRepository> account_repository,
    shared_ptr<TransactionRepository> transaction_repository,
    shared_ptr<Account> account,
    shared_ptr<Transaction> transaction
) {
    this->account_repository = account_repository;
    this->transaction_repository = transaction_repository;
    this->account = account;
    this->transaction = transaction;
}

void BankService::run_app() {
    int choice = 0;

    while(true)
    {
        this->show_menu();

        cout << "\nYour choice: ";
        cin >> choice;

        switch(choice)
        {
            case this->CHOICE_ACCOUNT_DETAILS:
                this->show_account_details();
                break;
            case this->CHOICE_DEPOSIT:
                this->deposit_money();
                break;
            case this->CHOICE_WITHDRAW:
                this->withdraw_money();
                break;
            case this->CHOICE_TRANSACTION:
                this->show_transaction_details();
                break;
            case this->CHOICE_EXIT:
                exit(0);
                break;
            default:
                cout << "Invalid Choice \n";
        }
    }
}

void BankService::show_menu() {
    cout << "\nMENU\n";
    cout << "---------\n";

    cout << "\n1: Account Details";
    cout << "\n2: Deposit Money";
    cout << "\n3: Withdraw Money";
    cout << "\n4: Transaction Details";
    cout << "\n5: Exit\n";
}

void BankService::show_account_details() {
    cout << "\nAcount Details\n";
    cout << "--------------\n\n";

    cout << "Name: " << this->account->get_owner() << "\n";
    cout << "Pin: " << this->account->get_pin() << "\n";
    cout << "Phone: " << this->account->get_phone() << "\n";
    cout << "Email: " << this->account->get_email() << "\n";
    cout << "Registration date: " << this->account->get_registration_date() << "\n";
    cout << "Balance: " << this->account->get_balance() << "\n";

    show_press_any_key();
}

void BankService::deposit_money() {
    cout << "\nDeposit Money\n";
    cout << "--------------\n\n";

    double amount = 0;

    cout << "Enter amount: ";
    cin >> amount;
    // round the number to two decimals
    amount = floor(amount * 100.0) / 100.0;

    try {
        this->account_repository->update_balance(amount, this->account->get_id());
        this->transaction->Init(amount, account->get_id(), "deposit");
        this->transaction_repository->create(*this->transaction);
        this->account->set_balance(this->account->get_balance() + amount);

        cout << "Successfully deposited\n";
    }
    catch(CreateException) {
        cout << "There was a problem while creating the transaction\n";
    }
    catch(UpdateException) {
        cout << "There was a problem while updating the balance\n";
    }
    catch(exception) {
        cout << "There was a problem while depositing\n";
    }

    show_press_any_key();
}

void BankService::withdraw_money() {
    cout << "\nWithdraw Money\n";
    cout << "--------------\n\n";

    double amount = 0;

    cout << "Enter amount: ";
    cin >> amount;
    // round the number to two decimals
    amount = floor(amount * 100.0) / 100.0;

    if (amount > this->account->get_balance()) {
        cout << "\nNot enough money on the account\n";

        this->show_press_any_key();

        return;
    }

    try {
        this->account_repository->update_balance(-amount, this->account->get_id());
        this->transaction->Init(-amount, this->account->get_id(), "withdraw");
        this->transaction_repository->create(*this->transaction);
        this->account->set_balance(this->account->get_balance() - amount);

        cout << "Successfully withdrawn\n";
    }
    catch(CreateException) {
        cout << "There was a problem while creating the transaction\n";
    }
    catch(UpdateException) {
        cout << "There was a problem while updating the balance\n";
    }
    catch(exception) {
        cout << "There was a problem while withdrawing\n";
    }

    this->show_press_any_key();
}

void BankService::show_transaction_details() {
    try {
        cout << "\nTransaction details\n";
        cout << "--------------\n\n";

        vector<Transaction> transactions = this->transaction_repository->find_by_account_id(account->get_id());

        if(transactions.size() == 0) {
            cout << "No transactions\n";

            return;
        }

         for(unsigned int i = 0; i < transactions.size(); i++) {
            cout << "Type: " << transactions[i].get_type() << endl;
            cout << "Amount: " << transactions[i].get_amount() << endl;
            cout << "Datetime: " << transactions[i].get_datetime() << endl;
            cout << "\n";
         }

         this->show_press_any_key();
    }
    catch(exception) {
        cout << "There was a problem while fetching transactions\n";
    }
}

void BankService::show_press_any_key() {
    cout << "\nPress Enter to continue… ";
    cin.get();
    cin.get();
}