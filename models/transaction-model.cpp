#include "transaction-model.h"

using namespace std;

Transaction::Transaction() {}
void Transaction::Init(
    double amount,
    int account_id,
    std::string type,
    std::string datetime,
    std::string account_owner
) {
    this->amount = amount;
    this->account_id = account_id;
    this->account_owner = account_owner;
    this->type = type;
    this->datetime = datetime;
}

double Transaction::get_amount() {
    return this->amount;
}

int Transaction::get_account_id() {
    return this->account_id;
}

string Transaction::get_type() {
    return this->type;
}

string Transaction::get_datetime() {
    return this->datetime;
}