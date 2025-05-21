<?php
namespace Mini\Db;

use Mini\Base\Exception;

class WpdbAdapter extends Db_Abstract
{
    /**
     * WordPress database object
     * @var \wpdb
     */
    protected $_dbh; // In Db_Abstract, _dbh is used for the connection object. We'll use it for $wpdb.

    /**
     * Constructor
     *
     * @param array $params (Largely ignored for $wpdb, but required by parent)
     */
    public function __construct($params = [])
    {
        global $wpdb;
        if (!isset($wpdb) || !is_object($wpdb)) {
            throw new Exception('WordPress global $wpdb is not available or not an object.');
        }
        $this->_dbh = $wpdb;

        // Satisfy parent constructor's basic requirements if it's called.
        // Db_Abstract requires dbname, username, passwd. We can provide placeholders.
        $dummyParams = [
            'host'     => $this->_dbh->dbhost,
            'dbname'   => $this->_dbh->dbname,
            'username' => $this->_dbh->dbuser,
            'passwd'   => $this->_dbh->dbpassword,
            'charset'  => $this->_dbh->charset ?? 'utf8',
            'persistent' => false, // $wpdb does not expose this directly in a simple way
        ];
        parent::__construct($dummyParams); // Call parent constructor
    }

    /**
     * Connect to the database.
     * For $wpdb, the connection is already managed by WordPress.
     */
    protected function _connect()
    {
        // Connection is handled by WordPress, so this is a no-op.
        // We've already assigned $wpdb to $this->_dbh in the constructor.
        if (!$this->_dbh) {
            throw new Exception('$wpdb object not initialized.');
        }
    }

    /**
     * Close the database connection.
     * For $wpdb, WordPress manages the connection lifecycle.
     */
    public function close()
    {
        // No-op, WordPress handles this.
        $this->_dbh = null; // Dereference, but WP keeps its own instance.
    }

    /**
     * Execute an SQL statement (typically for INSERT, UPDATE, DELETE)
     *
     * @param string $sql
     * @return int|false Number of rows affected/selected or false on error.
     */
    public function execSql($sql)
    {
        $this->_connect(); // Ensures _dbh is set (though it is from constructor)
        $this->_setLastSql($sql);
        if ($this->_debug === true) {
            $this->_debugSql($sql);
        }
        // $wpdb->query can return number of rows for DML, or false for error.
        $result = $this->_dbh->query($sql);
        if ($result === false) {
            $this->throwWpdbError();
        }
        return $result; // Returns number of affected rows
    }

    /**
     * Query SQL statement
     *
     * @param string $sql
     * @param string $queryMode 'all' or 'row'
     * @param array $binds (Not directly used by $wpdb in this simple wrapper, use $wpdb->prepare)
     * @return mixed
     */
    public function query($sql, $queryMode = 'all', $binds = [])
    {
        $this->_connect();
        
        // If binds are provided, we should attempt to prepare the statement.
        if (!empty($binds)) {
            // $wpdb->prepare needs specific formatting for placeholders (%s, %d, %f)
            // This simple version assumes $sql is already prepared or doesn't need it.
            // For a more robust solution, $sql would be a format string and $binds the values.
            // Example: $sql = "SELECT * FROM table WHERE column = %s AND another_column = %d"
            // $binds = ['value1', 123]
            // $prepared_sql = $this->_dbh->prepare($sql, ...$binds);
            // For now, we'll assume $sql is ready or $binds are not for $wpdb->prepare in this context.
            // A better implementation would adapt $binds to $wpdb->prepare syntax.
             $sql = $this->prepare($sql, $binds);
        }

        $this->_setLastSql($sql);
        if ($this->_debug === true) {
            $this->_debugSql($sql, $binds);
        }

        $queryMode = strtolower($queryMode);
        $result = null;

        if ($queryMode == 'all') {
            $result = $this->_dbh->get_results($sql, ARRAY_A);
        } elseif ($queryMode == 'row') {
            $result = $this->_dbh->get_row($sql, ARRAY_A);
        } else {
            // Potentially support other $wpdb->get_var, $wpdb->get_col if needed
            throw new Exception("Unsupported query mode '{$queryMode}'. Use 'all' or 'row'.");
        }

        if ($this->_dbh->last_error) {
            $this->throwWpdbError();
        }

        return $result;
    }

    /**
     * Insert a record
     *
     * @param string $table
     * @param array $data
     * @param boolean $prepare (Ignored, $wpdb->insert handles data type formatting via its own $format param)
     * @return int|false Number of rows inserted, or false on error.
     */
    public function insert($table, array $data, $prepare = true)
    {
        $this->_connect();
        $table = $this->ensureTablePrefix($table);
        $this->_setLastSql("INSERT INTO `$table` (keys) VALUES (values) with data: " . json_encode($data)); // Approximate SQL
        if ($this->_debug === true) {
            $this->_debugSql("INSERT INTO `$table` (keys) VALUES (values)", $data);
        }
        
        $result = $this->_dbh->insert($table, $data);

        if ($result === false) {
            $this->throwWpdbError();
        }
        return $result; // $wpdb->insert returns number of rows inserted.
    }
    
    /**
     * Insert multiple records
     * $wpdb doesn't have a direct "insertAll" like PDO batch.
     * This needs to be implemented by looping or constructing a complex query.
     * For simplicity, we'll loop, which is less efficient but functional.
     *
     * @param string $table
     * @param array $dataArray
     * @param boolean $prepare
     * @return int Total number of rows inserted or false on first error.
     */
    public function insertAll($table, array $dataArray, $prepare = true)
    {
        $this->_connect();
        $table = $this->ensureTablePrefix($table);
        $insertedCount = 0;
        // Note: This is not a true batch insert. $wpdb does not support it directly.
        // Each insert is a separate operation. For true batch, one would need to construct a single large SQL query.
        foreach ($dataArray as $data) {
            $result = $this->insert($table, $data, $prepare); // Uses the single insert method
            if ($result === false) { 
                // If one insert fails, we might want to stop or collect errors.
                // For now, return false to indicate failure.
                return false;
            }
            $insertedCount += $result;
        }
        return $insertedCount;
    }


    /**
     * Update records
     *
     * @param string $table
     * @param array $data
     * @param string $where (This is different from $wpdb, which takes an array for where)
     *                      We'll need to adapt or require $where to be an array for $wpdb.
     *                      For now, this implementation will be limited if $where is a string.
     *                      The abstract class defines $where as string.
     * @return int|false Number of rows updated, or false on error.
     */
    public function update($table, array $data, $where = '')
    {
        $this->_connect();
        $table = $this->ensureTablePrefix($table);
        // $wpdb->update expects $where to be an array like $data.
        // The abstract method defines $where as a string. This is a mismatch.
        // A simple approach for string $where:
        if (!is_array($where) && !empty($where)) {
            // This is not safe if $where contains user input.
            // $wpdb->update is safer with array $where.
            // For now, we'll construct a query. This is less ideal.
            $sql = "UPDATE `$table` SET ";
            $setClauses = [];
            foreach ($data as $column => $value) {
                // This is a simplified example; proper escaping/preparation is crucial.
                $setClauses[] = "`$column` = '" . $this->_dbh->escape($value) . "'";
            }
            $sql .= implode(', ', $setClauses);
            $sql .= " WHERE " . $where;
            $this->_setLastSql($sql);
            if ($this->_debug === true) {
                $this->_debugSql($sql);
            }
            $result = $this->_dbh->query($sql);
        } else if (is_array($where)) {
             // If $where is an array, use $wpdb->update directly
            $this->_setLastSql("UPDATE `$table` SET (data) WHERE (where_array) with data: " . json_encode($data) . " and where: " . json_encode($where));
            if ($this->_debug === true) {
                 $this->_debugSql("UPDATE `$table` SET ... WHERE ...", ['data' => $data, 'where' => $where]);
            }
            $result = $this->_dbh->update($table, $data, $where);
        } else { // No WHERE clause, update all rows (dangerous, but $wpdb->update supports it if $where is empty)
            $this->_setLastSql("UPDATE `$table` SET (data) with data: " . json_encode($data));
             if ($this->_debug === true) {
                 $this->_debugSql("UPDATE `$table` SET ...", ['data' => $data]);
            }
            $result = $this->_dbh->update($table, $data, []); // Empty array for where
        }


        if ($result === false) {
            $this->throwWpdbError();
        }
        return $result;
    }

    /**
     * Replace a record
     * $wpdb->replace is available.
     *
     * @param string $table
     * @param array $data
     * @return int|false
     */
    public function replace($table, array $data)
    {
        $this->_connect();
        $table = $this->ensureTablePrefix($table);
        $this->_setLastSql("REPLACE INTO `$table` (keys) VALUES (values) with data: " . json_encode($data));
        if ($this->_debug === true) {
            $this->_debugSql("REPLACE INTO `$table` ...", $data);
        }
        $result = $this->_dbh->replace($table, $data);
        if ($result === false) {
            $this->throwWpdbError();
        }
        return $result;
    }

    /**
     * Delete records
     *
     * @param string $table
     * @param string $where (Similar to update, $wpdb->delete expects an array for $where)
     * @return int|false Number of rows deleted, or false on error.
     */
    public function delete($table, $where = '')
    {
        $this->_connect();
        $table = $this->ensureTablePrefix($table);
        // Similar issue as with update(): $where is string in abstract, array in $wpdb->delete.
        if (!is_array($where) && !empty($where)) {
            $sql = "DELETE FROM `$table` WHERE " . $where;
            $this->_setLastSql($sql);
            if ($this->_debug === true) {
                $this->_debugSql($sql);
            }
            $result = $this->_dbh->query($sql);
        } else if (is_array($where)) {
            $this->_setLastSql("DELETE FROM `$table` WHERE (where_array) with where: " . json_encode($where));
            if ($this->_debug === true) {
                $this->_debugSql("DELETE FROM `$table` WHERE ...", $where);
            }
            $result = $this->_dbh->delete($table, $where);
        } else { // No WHERE clause, delete all rows (dangerous!)
             // $wpdb->delete requires a non-empty where. To delete all, must pass something like array('1' => '1')
             // For safety, we can throw an exception or require a specific action.
            throw new Exception("Attempting to delete all rows from table '$table'. Please provide a WHERE clause or use a specific method for this.");
        }

        if ($result === false) {
            $this->throwWpdbError();
        }
        return $result;
    }

    /**
     * Count rows in a table
     *
     * @param string $table
     * @param string $col
     * @param string $where
     * @return int
     */
    public function countRow($table, $col = '*', $where = '')
    {
        $this->_connect();
        $table = $this->ensureTablePrefix($table);
        // $col is not directly used by $wpdb count. $wpdb counts all matching rows.
        // For $wpdb, it's more common to just use a SELECT COUNT(*) query.
        $sql = "SELECT COUNT({$col}) FROM `{$table}`";
        if (!empty($where)) {
            $sql .= " WHERE {$where}";
        }
        $this->_setLastSql($sql);
        if ($this->_debug === true) {
            $this->_debugSql($sql);
        }
        $count = $this->_dbh->get_var($sql);
        if ($count === null && $this->_dbh->last_error) { // Check for null result due to error
            $this->throwWpdbError();
        }
        return (int)$count;
    }

    /**
     * Begin a transaction
     */
    protected function _beginTransaction()
    {
        $this->_connect();
        $this->_dbh->query('START TRANSACTION');
        // $this->_dbh->beginTransaction(); // $wpdb does not have this method directly.
    }

    /**
     * Commit a transaction
     */
    protected function _commit()
    {
        $this->_connect();
        $this->_dbh->query('COMMIT');
        // $this->_dbh->commit(); // $wpdb does not have this method directly.
    }

    /**
     * Roll back a transaction
     */
    protected function _rollBack()
    {
        $this->_connect();
        $this->_dbh->query('ROLLBACK');
        // $this->_dbh->rollBack(); // $wpdb does not have this method directly.
    }

    /**
     * Get the ID of the last inserted row
     *
     * @return int
     */
    public function lastInsertId()
    {
        $this->_connect();
        return $this->_dbh->insert_id;
    }
    
    /**
     * Prepares a SQL query for safe execution.
     * Uses $wpdb->prepare().
     *
     * @param string $query Query statement with sprintf-like placeholders (%s, %d, %f).
     * @param array|mixed $args The array of values to replace placeholders, or single value for one placeholder.
     * @return string|void The prepared query, or void if an error occurred.
     */
    public function prepare($query, $args)
    {
        $this->_connect();
        if ( null === $query ) {
            return;
        }
        // $wpdb->prepare expects arguments to be passed as individual parameters, not an array.
        // So, we use the spread operator (...) if $args is an array.
        if (is_array($args)) {
            $prepared_sql = $this->_dbh->prepare($query, ...$args);
        } else {
            $prepared_sql = $this->_dbh->prepare($query, $args);
        }

        if ( null === $prepared_sql ) { // $wpdb->prepare can return null on error (e.g. too few arguments)
            throw new Exception( '$wpdb->prepare failed. Check query and arguments. Last error: ' . $this->_dbh->last_error );
        }
        return $prepared_sql;
    }

    /**
     * Get the WordPress database table prefix.
     *
     * @return string
     */
    public function getTablePrefix()
    {
        return $this->_dbh->prefix;
    }

    /**
     * Ensures the table name has the WordPress prefix.
     * If the table name already starts with the prefix, it's returned unchanged.
     *
     * @param string $table The table name.
     * @return string The table name with the WordPress prefix.
     */
    protected function ensureTablePrefix($table)
    {
        if (strpos($table, $this->_dbh->prefix) !== 0) {
            return $this->_dbh->prefix . $table;
        }
        return $table;
    }

    /**
     * Throws an exception based on $wpdb->last_error.
     */
    protected function throwWpdbError()
    {
        $error = $this->_dbh->last_error;
        // You might also want to check $this->_dbh->last_query for context
        throw new Exception("WordPress DB Error: " . $error);
    }
    
    // Methods from Db_Abstract that might not be perfectly aligned or needed with $wpdb:
    // - getMaxValue: Can be implemented with get_var and MAX().
    // - checkTableIsExist: Can be implemented with $wpdb->get_var("SHOW TABLES LIKE '...'").
    // - getTableEngine: Specific to MySQL, might need a custom query.
    // - execTrans: Db_Abstract has this, $wpdb does not. Can be implemented by wrapping calls in transaction methods.

    // Public version of _setLastSql if needed for debugging or logging outside
    public function setLastSql($sql = null)
    {
        $this->_setLastSql($sql);
    }

    /**
     * Get the last database error message.
     *
     * @return string
     */
    public function getLastError()
    {
        if ($this->_dbh) {
            return $this->_dbh->last_error;
        }
        return 'Database handler not initialized.';
    }
}

?>
