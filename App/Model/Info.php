<?php
namespace App\Model;

use Mini\Base\Model;
//use Mini\Base\Config;
//use Mini\Db\Db; // 工厂模式
//use Mini\Db\Mysql; // 直接调用

/**
 * 这是一个模型的案例
 * MiniFramework 从 1.0.0 开始全面启用了命名空间，创建模型时，需在文件顶部放置 namespace App\Model; 进行声明。
 */
class Info extends Model
{
    public function getWordPressInfo()
    {
        // $this->_db is initialized in the Model's constructor via App::loadDb('default')
        // which should now be the WpdbAdapter.
        // The parent Model class (Mini\Base\Model) constructor handles this:
        // if (DB_AUTO_CONNECT === true && $db === null) {
        //     $db = $this->loadDb('default');
        // }
        // if ($db) {
        //     parent::__construct($db); // parent is Query, which stores $db in $this->_db
        // }

        if (!$this->_db) {
            return 'Error: Database connection not available in Info Model.';
        }

        // Example 1: Get WordPress site URL from options table
        $prefix = $this->_db->getTablePrefix(); // WpdbAdapter has getTablePrefix()
        $sql = "SELECT option_value FROM {$prefix}options WHERE option_name = 'siteurl'";
        
        // Use query($sql, 'row') as per Db_Abstract and WpdbAdapter implementation
        $result = $this->_db->query($sql, 'row'); 

        if ($result) {
            return 'Site URL from WP options: ' . (is_array($result) ? $result['option_value'] : $result->option_value);
        } else {
            // Example 2: If options table access is complex or fails, try DB version as a fallback test
            // $sqlVersion = "SELECT @@VERSION as version";
            // $versionResult = $this->_db->query($sqlVersion, 'row');
            // if ($versionResult) {
            //    return 'Database Version: ' . (is_array($versionResult) ? $versionResult['version'] : $versionResult->version);
            // }
            
            // WpdbAdapter now has getLastError()
            $lastError = $this->_db->getLastError(); 
            return 'Could not fetch site URL. DB Last Error: ' . ($lastError ? $lastError : 'No specific error message.');
        }
    }
}
