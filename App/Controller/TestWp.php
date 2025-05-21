<?php
namespace App\Controller;

use Mini\Base\Controller; // Updated use statement
use App\Model\Info; // Assuming 'App' namespace is autoloaded for the App/ directory

class TestWp extends Controller // Updated base class
{
    public function index() // Renamed method
    {
        // The View object ($this->view) is automatically created by Mini\Base\Controller
        // The constructor of Controller calls $this->initView();
        // $this->initView() creates $this->view = new \Mini\Base\View();

        $infoModel = new Info();
        $wpData = $infoModel->getWordPressInfo();

        $this->view->assign('wp_data', $wpData);
        
        // Generate the URL for the current page using mf_plugin_url
        // mf_plugin_url is defined in MiniFramework/Function/Global.func.php
        $current_page_params = [
            'mf_controller' => 'testwp', // Current controller
            'mf_action' => 'index'       // Current action
            // Add any other relevant parameters if needed for the link
        ];
        $this->view->assign('plugin_page_url', mf_plugin_url($current_page_params));
        
        $this->view->display();
    }
}
?>
