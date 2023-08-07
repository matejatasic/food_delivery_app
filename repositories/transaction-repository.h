#pragma once
#include <sqlite3.h>
#include <vector>
#include "../models/transaction-model.h"

class TransactionRepository {
    private:
        sqlite3 *db;
        sqlite3_stmt* stmt;
        int result;
        std::string const table_name = "transactions";
    public:
        TransactionRepository();
        ~TransactionRepository();
        void create(Transaction transaction);
        std::vector<Transaction> find_by_account_id(int account_id);
};