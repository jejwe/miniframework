# Miniframework WordPress 插件集成指南

## 1. 简介 (Introduction)

此版本的 Miniframework 已被特别重构，以支持作为 WordPress 插件进行无缝集成和开发。这意味着您可以在熟悉的 WordPress 环境中，继续利用 Miniframework 清晰的 MVC (Model-View-Controller) 结构、高效的路由机制以及便捷的开发方式来构建功能丰富的插件。

这种集成保留了 Miniframework 的核心优势，如：
*   **清晰的MVC架构**：帮助分离业务逻辑、数据处理和用户界面。
*   **面向对象的开发**：鼓励编写模块化、可重用的代码。
*   **灵活的扩展性**：方便添加自定义功能和库。

## 2. 安装与启用 (Installation and Activation)

将 Miniframework 作为 WordPress 插件安装非常简单：

1.  **复制文件**: 将整个 Miniframework 项目文件夹（包含 `App/`, `MiniFramework/` 和 `miniframework-plugin.php` 等）复制到您的 WordPress 安装目录下的 `wp-content/plugins/` 文件夹中。您可以将项目文件夹重命名为您插件的名称，例如 `my-miniframework-plugin`。
2.  **后台激活**:
    *   登录到您的 WordPress 后台。
    *   导航到 “插件” 页面。
    *   在插件列表中找到您刚刚添加的 Miniframework 插件。
    *   点击 “激活” 链接。

激活后，插件的主入口文件 `miniframework-plugin.php` 将负责初始化和运行 Miniframework 应用。

## 3. 核心变化 (Core Changes)

为了适应 WordPress 环境，Miniframework 在以下几个核心方面进行了调整：

### 入口文件 (Entry Point)

*   **新的唯一入口点**: `miniframework-plugin.php` 文件现在是框架作为 WordPress 插件运行时的唯一入口点。所有对框架的请求都将间接通过此文件由 WordPress 处理。
*   **原有入口废弃**: 之前在独立模式下使用的 `App/Public/index.php` (以及 `index-dev.php`, `index-test.php`) 文件不再作为直接的Web访问入口。

### URL 与路由 (URL and Routing)

*   **WordPress 生成 URL**: 插件的后台管理页面 URL 现在由 WordPress 生成。例如，在 `miniframework-plugin.php` 中通过 `add_menu_page` 创建的主菜单页面，其基础 URL 通常类似于 `wp-admin/admin.php?page=miniframework-main-page` (其中 `miniframework-main-page` 是菜单的 slug)。
*   **GET 参数指定路由**: Miniframework 的控制器 (Controller) 和动作 (Action) 通过特定的 GET 请求参数 `mf_controller` 和 `mf_action` 来指定。
    *   例如: `wp-admin/admin.php?page=miniframework-main-page&mf_controller=mycontroller&mf_action=myaction`
    *   这将路由到 `App/Controller/Mycontroller.php` 中的 `myaction()` 方法 (注意：`Action` 后缀已从方法名中移除)。
*   **辅助函数 `mf_plugin_url()`**: 为了方便生成插件内部的正确链接（例如，在视图中链接到其他控制器/动作），框架提供了一个名为 `mf_plugin_url(array $params = [], $page_slug = null)` 的辅助函数。此函数定义在 `MiniFramework/Function/Global.func.php` 中。
    *   示例用法: `echo mf_plugin_url(['mf_controller' => 'user', 'mf_action' => 'list']);`
*   **`.htaccess` 无效**: Miniframework 自带的用于 URL 重写的 `.htaccess` 文件（通常位于 `App/Public/` 目录下）在 WordPress 插件模式下是无效的。所有 URL 解析和路由现在完全由 WordPress 的查询参数机制处理。

### 数据库 (Database)

*   **自动使用 `$wpdb`**: 框架现在会自动配置并使用 WordPress 的全局数据库对象 `$wpdb` 来执行所有数据库操作。
*   **`WpdbAdapter` 包装器**: 当您通过 `App::loadDb('default')` 或在模型中使用 `$this->_db` (由 `Mini\Base\Model` 初始化) 时，获取到的数据库实例实际上是 `$wpdb` 的一个包装器，即 `Mini\Db\WpdbAdapter`。这个适配器将 Miniframework 的数据库方法调用转换为相应的 `$wpdb` 方法。
*   **模型层兼容性**: 大多数情况下，您在模型层编写的数据库操作代码（如使用 `$this->_db->insert()`, `$this->_db->query()`, `$this->_db->update()` 等）无需修改，可以继续像在独立 Miniframework 应用中那样使用。`WpdbAdapter` 会处理底层的转换。

### 静态资源 (Static Assets - CSS, JS)

*   **WordPress 排队机制**: 插件的 CSS 和 JavaScript 文件应通过 WordPress 的标准排队机制加载。
*   **`miniframework_enqueue_plugin_assets` 函数**: 在 `miniframework-plugin.php` 文件中，提供了一个示例函数 `miniframework_enqueue_plugin_assets($hook_suffix)`，它被挂载到 `admin_enqueue_scripts` 动作钩子上。
*   **`wp_enqueue_style` 和 `wp_enqueue_script`**: 在此函数内部，您应该使用 `wp_enqueue_style()` 来加载 CSS 文件，使用 `wp_enqueue_script()` 来加载 JavaScript 文件。
*   **`plugins_url()` 生成 URL**: 必须使用 `plugins_url('path/to/asset', __FILE__)` 函数来生成指向位于插件目录内静态资源的正确 URL。例如，`plugins_url('App/Public/css/default.css', __FILE__)`。
*   **按需加载**: 建议在 `miniframework_enqueue_plugin_assets` 函数中检查当前的 `$hook_suffix`，以确保您的静态资源仅在插件自己的管理页面加载，避免不必要的全局加载。

### 配置 (Configuration)

*   **集中到插件文件**: Miniframework 的主要配置（例如特性开关、路径常量等）已移至主插件文件 `miniframework-plugin.php` 的顶部。
*   **覆盖默认设置**: 这些常量（如 `DB_AUTO_CONNECT`, `LAYOUT_ON`, `SHOW_ERROR`, `PUBLIC_PATH` 等）在 `MiniFramework/Bootstrap.php` 文件加载 *之前* 定义。由于 `Bootstrap.php` 中的常量定义使用了 `defined('CONSTANT_NAME') || define(...);` 的模式，因此在 `miniframework-plugin.php` 中定义的这些值将有效覆盖框架的默认设置，从而使框架适应 WordPress 环境。

## 4. 目录结构 (Directory Structure)

集成为 WordPress 插件后，项目的主要目录结构及其用途如下：

*   **`App/`**: 此目录依然是您应用的核心。
    *   `Controller/`: 存放控制器类。
    *   `Model/`: 存放模型类。
    *   `View/`: 存放视图文件。
    *   `Public/`: 此目录不再包含 `index.php` 入口文件或 `.htaccess` 规则。它现在主要用于存放静态资源（如 CSS, JS, images），这些资源将通过 WordPress 的排队机制从 `miniframework-plugin.php` 中加载。
    *   其他如 `Config/`, `Lang/` 等目录的使用方式保持不变。
*   **`MiniFramework/`**: 包含 Miniframework 的核心类和文件。通常您不需要修改此目录的内容。
*   **`miniframework-plugin.php`**: 这是新的 WordPress 插件主文件。它负责：
    *   定义插件头信息。
    *   设置 Miniframework 的配置常量。
    *   包含 `MiniFramework/Bootstrap.php` 来启动框架。
    *   注册 WordPress 的动作钩子（如 `admin_menu` 用于创建菜单，`admin_enqueue_scripts` 用于加载资源）。
    *   作为 Miniframework 应用在 WordPress 环境中的主要协调者。

## 5. 开发实践 (Development Practices)

以下是在此集成环境中进行开发的一些关键实践：

### 创建页面 (Admin Pages)

1.  **注册菜单**: 在 `miniframework-plugin.php` 中，使用 WordPress 函数 `add_menu_page()` (用于顶级菜单) 或 `add_submenu_page()` (用于子菜单) 来注册您的插件管理页面。
2.  **指定回调函数**: 为菜单注册指定一个回调函数。
3.  **启动 Miniframework**: 在该回调函数中：
    *   获取 `App` 实例: `$app = \Mini\Base\App::getInstance();`
    *   获取 `Router` 实例并设置路由类型为 'wordpress': `$router = $app->getRouter(); $router->setRouteType('wordpress');`
    *   调用 `$app->run();` 来处理请求并执行相应的 Miniframework 控制器和动作。

### 控制器 (Controllers)

*   在 `App/Controller/` 目录下创建您的控制器类。
*   控制器类应继承自 `\Mini\Base\Controller`。
*   控制器中的方法（动作）名称直接对应路由中的动作名，不再需要 `Action` 后缀。例如，如果动作是 `index`，则方法名为 `index()`；如果动作是 `listUsers`，则方法名为 `listUsers()`。
*   可以通过 `$this->view` 访问视图对象。

### 模型 (Models)

*   在 `App/Model/` 目录下创建您的模型类。
*   模型类通常继承自 `\Mini\Base\Model` (或不继承，直接使用 `App::loadDb('default')`)。
*   在模型方法中，可以通过 `$this->_db` (如果继承自 `\Mini\Base\Model`，它会在构造函数中被初始化为 `WpdbAdapter` 实例) 来执行数据库操作。

### 视图 (Views)

*   视图文件应放置在 `App/View/controllername/actionname.php` 路径下，其中 `controllername` 是控制器名称的小写形式（不含 "Controller" 后缀），`actionname` 是动作名称的小写形式。
*   在控制器中，使用 `$this->view->assign('variableName', $value);` 将数据从控制器传递到视图。
*   在控制器中，调用 `$this->view->display();` 来渲染并显示相应的视图文件。
*   在视图文件中，可以通过 `$this->variableName` 来访问传递过来的数据。
*   使用 `mf_plugin_url([...])` 辅助函数生成指向插件内部其他页面的链接。

### 安全 (Security)

*   **WordPress Nonces**: 对于执行数据修改、删除等敏感操作的请求，强烈建议使用 WordPress Nonces (Number used once) 来防止 CSRF (Cross-Site Request Forgery) 攻击。
*   **权限检查**: 使用 WordPress 的 `current_user_can('capability_name')` 函数来检查当前用户是否拥有执行特定操作所需的权限。
*   **`CSRF_TOKEN_ON` 配置**: 在 `miniframework-plugin.php` 中，Miniframework 自带的 CSRF 保护功能已通过 `define('CSRF_TOKEN_ON', false);` 默认关闭，以便优先使用 WordPress 的安全机制。
*   **数据校验与清理**: 对所有用户输入数据进行严格的校验 (Validation) 和清理 (Sanitization)。

## 6. 示例 (Example)

本项目中的 `App/Controller/TestWp.php` 控制器、`App/Model/Info.php` 模型中的 `getWordPressInfo()` 方法以及 `App/View/testwp/index.php` 视图提供了一个基本的工作示例。您可以参考这些文件来了解如何在 WordPress 集成环境中设置和使用 Miniframework 的 MVC 组件。

*   **TestWp 控制器**: 演示了如何实例化模型、调用模型方法、将数据传递给视图以及如何使用 `mf_plugin_url()`。
*   **Info 模型 (`getWordPressInfo` 方法)**: 演示了如何通过 `$this->_db` (即 `WpdbAdapter`) 与 WordPress 数据库交互，例如获取表前缀和查询 `wp_options` 表。
*   **testwp/index.php 视图**: 演示了如何在视图中显示从控制器传递的数据和生成的链接。

## 7. 注意事项 (Important Notes)

*   **`PUBLIC_PATH` 的用途**: 虽然 `PUBLIC_PATH` 常量在 `miniframework-plugin.php` 中被定义为指向插件内部的 `App/Public/` 目录，但在 WordPress 环境中，静态资源（CSS, JS, 图片等）主要通过 `wp_enqueue_style`/`wp_enqueue_script` 和 `plugins_url()` 机制来提供服务和访问。直接依赖 `PUBLIC_PATH` 进行 URL 拼接可能不适用于所有情况。
*   **框架特性评估**: 原 Miniframework 的某些特性，例如其独立的 REST API 模式 (`REST_ON`) 或直接文件写入的日志系统 (`LOG_ON` 设为文件模式时)，在 WordPress 环境中可能需要重新评估其适用性或进行额外配置。例如，REST API 可以考虑使用 WordPress 的 REST API 框架，日志可以考虑集成到 WordPress 的错误处理或使用更通用的日志库。
*   **WordPress API 优先**: 在开发插件时，如果 WordPress 提供了相应功能的 API (例如用户管理、权限、设置、HTTP请求等)，建议优先使用 WordPress 的 API，以确保最佳的兼容性和安全性。

希望本指南能帮助您顺利地使用 Miniframework 在 WordPress 平台上进行插件开发！
