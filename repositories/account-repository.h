#pragma once
#include <sqlite3.h>
#include <string>
#include <memory>
#include "../models/account-model.h"

class  AccountRepository {
    private:
        sqlite3 *db;
        sqlite3_stmt* stmt;
        int result;
        bool table_exists();
        std::shared_ptr<Account> account;
        std::string const table_name = "accounts";
    public:
        AccountRepository(std::shared_ptr<Account> account);
        ~AccountRepository();
        std::shared_ptr<Account> find_by_owner(std::string name);
        void update_balance(double balance_change, int account_id);
};