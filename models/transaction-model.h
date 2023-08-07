#include <string>

class Transaction {
    private:
        double amount;
        int account_id;
        std::string type;
        std::string datetime;
        std::string account_owner;

    public:
        Transaction();
        void Init(
            double amount,
            int account_id,
            std::string type,
            std::string datetime = "",
            std::string account_owner = ""
        );

        double get_amount();
        int get_account_id();
        std::string get_type();
        std::string get_datetime();
};