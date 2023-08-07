class DatabaseOpenException : public std::exception {};

class TableDoesNotExistException : public std::exception {};

class RecordNotFound : public std::exception {};

class CreateException : public std::exception {};

class UpdateException : public std::exception {};