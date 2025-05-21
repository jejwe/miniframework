<?php
/**
 * Plugin Name: Miniframework Integration
 * Description: Integrates the Miniframework with WordPress.
 * Version: 1.0
 * Author: Your Name
 */

// Prevent direct access
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Define APP_NAMESPACE if not already defined
defined('APP_NAMESPACE') || define('APP_NAMESPACE', 'App');

// Define MINI_PATH (Path to MiniFramework directory)
// Assumes miniframework-plugin.php is in the plugin's root directory, 
// and MiniFramework is a subdirectory.
defined('MINI_PATH') || define('MINI_PATH', plugin_dir_path(__FILE__) . 'MiniFramework');

// Define APP_PATH (Path to App directory)
// Assumes App is a subdirectory in the plugin's root.
defined('APP_PATH') || define('APP_PATH', plugin_dir_path(__FILE__) . 'App');

// Define the main page slug for the plugin
defined('MINIFRAMEWORK_MAIN_SLUG') || define('MINIFRAMEWORK_MAIN_SLUG', 'miniframework-main-page');


// --- Miniframework Specific Configurations for WordPress ---

// Core Paths like APP_NAMESPACE, MINI_PATH, APP_PATH are already defined above and are correct.

// WordPress-aware PUBLIC_PATH for assets.
// This path points to the App/Public directory within the plugin.
// Actual asset serving should use plugins_url() and WordPress enqueue functions.
defined('PUBLIC_PATH') || define('PUBLIC_PATH', APP_PATH . DIRECTORY_SEPARATOR . 'Public');

// Feature Flags
defined('LAYOUT_ON') || define('LAYOUT_ON', true); // Enable layout system
defined('TPL_ON') || define('TPL_ON', true);      // Enable template engine (if used by the framework, e.g. for .tpl files)
defined('REST_ON') || define('REST_ON', false);   // Disable REST API features by default for WP integration
defined('LOG_ON') || define('LOG_ON', false);    // Disable logging by default
defined('CSRF_TOKEN_ON') || define('CSRF_TOKEN_ON', false); // Disable built-in CSRF, rely on WP nonces
defined('DB_AUTO_CONNECT') || define('DB_AUTO_CONNECT', true); // Enable auto-connection to DB (uses $wpdb via WpdbAdapter)

// Error Reporting & Debugging (recommended for development)
defined('APP_ENV') || define('APP_ENV', 'dev');        // Application environment: 'dev' or 'prod'
defined('SHOW_ERROR') || define('SHOW_ERROR', true);   // Show detailed error messages
defined('SHOW_DEBUG') || define('SHOW_DEBUG', true);   // Show framework's specific debug information
defined('ERROR_PAGE') || define('ERROR_PAGE', 'error/index'); // Custom error page route (e.g., 'ErrorController/indexAction')

// --- End Miniframework Specific Configurations ---


// Include the Miniframework bootstrap
if (file_exists(MINI_PATH . '/Bootstrap.php')) {
    require_once MINI_PATH . '/Bootstrap.php';
} else {
    // Handle error: Bootstrap file not found
    wp_die('Miniframework Bootstrap.php not found. Expected at: ' . MINI_PATH . '/Bootstrap.php');
}

// Example WordPress hook
function miniframework_plugin_admin_menu() {
    add_menu_page(
        'Miniframework Plugin',
        'Miniframework',
        'manage_options',
        MINIFRAMEWORK_MAIN_SLUG, // Use the defined constant here
        'miniframework_render_page_callback'
    );
}
add_action('admin_menu', 'miniframework_plugin_admin_menu');

// Placeholder for the page rendering callback
function miniframework_render_page_callback() {
    echo "<h1>Miniframework Page</h1>";

    // Get the App instance
    $app = \Mini\Base\App::getInstance();

    // Get the router instance that the App will use
    // App::getRouter() will create a router instance if it doesn't exist.
    $router = $app->getRouter();
    
    // Explicitly set the route type to 'wordpress'
    // This tells the router to look for 'mf_controller' and 'mf_action' in $_GET
    // when its route() method is called (which happens inside $app->run()).
    $router->setRouteType('wordpress'); 

    // Note: DB_AUTO_CONNECT, CSRF_TOKEN_ON, LOG_ON, REST_ON were moved
    // to the configuration block before Bootstrap.php is included.

    // The App's run() method will then use this router instance,
    // which will parse mf_controller and mf_action.
    try {
        // The run() method should trigger the router, load the controller, and execute the action.
        $app->run();
    } catch (\Mini\Base\Exception $e) {
        // Handle Miniframework specific exceptions
        // You might want to log these or display them more nicely depending on WP_DEBUG.
        wp_die('Miniframework Error: <pre>' . esc_html($e->getMessage()) . '</pre><p>Trace: <pre>' . esc_html($e->getTraceAsString()) . '</pre></p>');
    } catch (\Exception $e) {
        // Handle other general exceptions
        wp_die('General Error: <pre>' . esc_html($e->getMessage()) . '</pre><p>Trace: <pre>' . esc_html($e->getTraceAsString()) . '</pre></p>');
    }
}

// Enqueue plugin assets (CSS and JavaScript)
function miniframework_enqueue_plugin_assets($hook_suffix) {
    // $hook_suffix is the unique suffix for the admin page.
    // For a top-level page created by add_menu_page, the hook suffix is 'toplevel_page_YOUR_MENU_SLUG'.
    // MINIFRAMEWORK_MAIN_SLUG should be defined and hold our menu slug.
    if (!defined('MINIFRAMEWORK_MAIN_SLUG')) {
        // Fallback or error if the slug constant isn't defined, though it should be.
        // error_log('MINIFRAMEWORK_MAIN_SLUG is not defined. Cannot enqueue assets specifically.');
        return;
    }
    
    $plugin_page_hook_name = 'toplevel_page_' . MINIFRAMEWORK_MAIN_SLUG;

    // Only load assets on our plugin's page
    if ($hook_suffix == $plugin_page_hook_name) {
        // Enqueue Style
        wp_enqueue_style(
            'miniframework-default-style', // Handle
            plugins_url('App/Public/css/default.css', __FILE__), // Path to CSS file
            [], // Dependencies
            '1.0.0' // Version
        );

        // Enqueue Script
        wp_enqueue_script(
            'miniframework-demo-script', // Handle
            plugins_url('App/Public/js/demo.js', __FILE__), // Path to JS file
            ['jquery'], // Dependencies (example: jQuery)
            '1.0.0', // Version
            true // Load in footer
        );
    }
}
add_action('admin_enqueue_scripts', 'miniframework_enqueue_plugin_assets');

?>
