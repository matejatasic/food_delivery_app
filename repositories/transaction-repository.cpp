#include <iostream>
#include "transaction-repository.h"
#include "../errors/errors.h"

using namespace std;

TransactionRepository::TransactionRepository() {
    int conn = sqlite3_open("bank-management-system.db", &this->db);
}

TransactionRepository::~TransactionRepository() {
    sqlite3_close(this->db);
}

void TransactionRepository::create(Transaction transaction) {
    const string query = "INSERT INTO " + this->table_name + " (amount, account_id, type, datetime) VALUES(?, ?, ?, datetime('now'))";
    this->result = sqlite3_prepare(this->db, query.c_str(), query.length(), &this->stmt, NULL);

    if (this->result != SQLITE_OK) {
        throw exception();
    }

    sqlite3_bind_double(this->stmt, 1, transaction.get_amount());
    sqlite3_bind_int(this->stmt, 2, transaction.get_account_id());
    sqlite3_bind_text(this->stmt, 3, transaction.get_type().c_str(), -1, SQLITE_TRANSIENT);

    this->result = sqlite3_step(this->stmt);
    sqlite3_finalize(this->stmt);

    if (this->result != SQLITE_DONE) {
        throw CreateException();
    }
}

vector<Transaction> TransactionRepository::find_by_account_id(int account_id) {
    const string query = "SELECT amount, type, datetime FROM " + this->table_name + " WHERE account_id=?";
    this->result = sqlite3_prepare(this->db, query.c_str(), query.length(), &this->stmt, NULL);

    if (this->result != SQLITE_OK) {
        throw exception();
    }

    sqlite3_bind_int(this->stmt, 1, account_id);

    vector<Transaction> transactions;

    while(sqlite3_step(this->stmt) == SQLITE_ROW) {
        const unsigned char* type_char = sqlite3_column_text(this->stmt, 1);
        const unsigned char* datetime_char = sqlite3_column_text(this->stmt, 2);

        double amount = sqlite3_column_double(this->stmt, 0);
        string type(reinterpret_cast< char const* >(type_char));
        string datetime(reinterpret_cast< char const* >(datetime_char));
        
        Transaction transaction;
        transaction.Init(amount, account_id, type, datetime);
        transactions.push_back(transaction);
    }

    sqlite3_finalize(this->stmt);

    return transactions;
}