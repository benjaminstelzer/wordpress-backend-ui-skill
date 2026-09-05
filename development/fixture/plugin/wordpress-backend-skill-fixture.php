<?php
/**
 * Plugin Name: WordPress Backend Skill Fixture
 * Description: Rendered acceptance fixture for the WordPress Backend UI Agent Skill.
 * Version: 1.0.0
 * Author: Benjamin Stelzer
 * License: MIT
 * License URI: https://opensource.org/license/mit
 * Requires at least: 7.0
 * Requires PHP: 8.1
 * Text Domain: wordpress-backend-skill-fixture
 * Domain Path: /languages
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const WBUI_FIXTURE_VERSION = '1.0.0';
const WBUI_FIXTURE_SLUG    = 'wordpress-backend-skill-fixture';
const WBUI_FIXTURE_HANDLE  = 'wordpress-backend-skill-fixture-app';
const WBUI_FIXTURE_TIMESTAMP = 1788436800; // 2026-09-03T12:00:00Z.

/**
 * Return the deterministic runtime mode requested by the acceptance fixture.
 *
 * @return string
 */
function wbui_fixture_get_mode() {
	$mode = isset( $_GET['wbui_mode'] ) ? sanitize_key( wp_unslash( $_GET['wbui_mode'] ) ) : 'hybrid';

	return in_array( $mode, array( 'classic', 'core', 'wpds', 'hybrid' ), true ) ? $mode : 'hybrid';
}

/**
 * Return the deterministic UI state requested by the acceptance fixture.
 *
 * @return string
 */
function wbui_fixture_get_state() {
	$state = isset( $_GET['wbui_state'] ) ? sanitize_key( wp_unslash( $_GET['wbui_state'] ) ) : 'initial';
	$states = array( 'initial', 'loading', 'partial', 'empty', 'success', 'error', 'disabled', 'permission' );

	return in_array( $state, $states, true ) ? $state : 'initial';
}

/**
 * Return the independent page-level Core Notice requested by the fixture.
 *
 * @return string
 */
function wbui_fixture_get_notice() {
	$notice  = isset( $_GET['wbui_notice'] ) ? sanitize_key( wp_unslash( $_GET['wbui_notice'] ) ) : 'none';
	$notices = array( 'none', 'partial', 'success', 'error' );

	return in_array( $notice, $notices, true ) ? $notice : 'none';
}

add_action(
	'init',
	static function () {
		load_plugin_textdomain(
			'wordpress-backend-skill-fixture',
			false,
			dirname( plugin_basename( __FILE__ ) ) . '/languages'
		);
	}
);

add_action(
	'admin_init',
	static function () {
		register_setting(
			'wbui_fixture_settings',
			'wbui_fixture_endpoint',
			array(
				'type'              => 'string',
				'sanitize_callback' => 'esc_url_raw',
				'default'           => '',
			)
		);

		add_settings_section(
			'wbui_fixture_connection',
			esc_html__( 'Connection', 'wordpress-backend-skill-fixture' ),
			static function () {
				echo '<p>' . esc_html__( 'Configure the endpoint used by this test fixture.', 'wordpress-backend-skill-fixture' ) . '</p>';
			},
			WBUI_FIXTURE_SLUG
		);

		add_settings_field(
			'wbui_fixture_endpoint',
			esc_html__( 'Endpoint URL', 'wordpress-backend-skill-fixture' ),
			static function () {
				$value = (string) get_option( 'wbui_fixture_endpoint', '' );
				?>
				<input
					id="wbui-fixture-endpoint"
					class="regular-text"
					type="url"
					name="wbui_fixture_endpoint"
					value="<?php echo esc_attr( $value ); ?>"
					aria-describedby="wbui-fixture-endpoint-description"
				>
				<p id="wbui-fixture-endpoint-description" class="description">
					<?php echo esc_html__( 'Enter the complete HTTPS endpoint.', 'wordpress-backend-skill-fixture' ); ?>
				</p>
				<?php
			},
			WBUI_FIXTURE_SLUG,
			'wbui_fixture_connection',
			array(
				'label_for' => 'wbui-fixture-endpoint',
			)
		);
	}
);

add_action(
	'admin_menu',
	static function () {
		add_options_page(
			esc_html__( 'Backend UI Fixture', 'wordpress-backend-skill-fixture' ),
			esc_html__( 'Backend UI Fixture', 'wordpress-backend-skill-fixture' ),
			'manage_options',
			WBUI_FIXTURE_SLUG,
			'wbui_fixture_render_page'
		);
	}
);

add_action(
	'network_admin_menu',
	static function () {
		add_submenu_page(
			'settings.php',
			esc_html__( 'Backend UI Fixture', 'wordpress-backend-skill-fixture' ),
			esc_html__( 'Backend UI Fixture', 'wordpress-backend-skill-fixture' ),
			'manage_network_options',
			WBUI_FIXTURE_SLUG,
			'wbui_fixture_render_page'
		);
	}
);

add_action(
	'admin_enqueue_scripts',
	static function ( $hook_suffix ) {
		if ( false === strpos( (string) $hook_suffix, WBUI_FIXTURE_SLUG ) ) {
			return;
		}
		if ( 'classic' === wbui_fixture_get_mode() ) {
			return;
		}

		$asset_file = plugin_dir_path( __FILE__ ) . 'build/index.asset.php';
		if ( ! file_exists( $asset_file ) ) {
			return;
		}
		$asset = require $asset_file;

		wp_register_script(
			WBUI_FIXTURE_HANDLE,
			plugins_url( 'build/index.js', __FILE__ ),
			$asset['dependencies'],
			$asset['version'],
			true
		);

		wp_set_script_translations(
			WBUI_FIXTURE_HANDLE,
			'wordpress-backend-skill-fixture',
			plugin_dir_path( __FILE__ ) . 'languages'
		);

		wp_localize_script(
			WBUI_FIXTURE_HANDLE,
			'wbuiFixtureData',
			array(
				'formattedNumber' => number_format_i18n( 12345.67, 2 ),
				'formattedDate'   => wp_date( get_option( 'date_format' ), WBUI_FIXTURE_TIMESTAMP ),
				'dateFormat'      => get_option( 'date_format' ),
				'fixtureDateIso'  => gmdate( 'c', WBUI_FIXTURE_TIMESTAMP ),
				'isNetworkAdmin'  => is_network_admin(),
				'mode'            => wbui_fixture_get_mode(),
				'state'           => wbui_fixture_get_state(),
				'dashboardUrl'    => is_network_admin() ? network_admin_url() : admin_url(),
			)
		);

		wp_enqueue_script( WBUI_FIXTURE_HANDLE );

		$token_style_file = plugin_dir_path( __FILE__ ) . 'build/design-tokens.css';
		if (
			in_array( wbui_fixture_get_mode(), array( 'wpds', 'hybrid' ), true ) &&
			file_exists( $token_style_file )
		) {
			wp_enqueue_style(
				'wordpress-backend-skill-fixture-tokens',
				plugins_url( 'build/design-tokens.css', __FILE__ ),
				array(),
				$asset['version']
			);
		}

		$style_file = plugin_dir_path( __FILE__ ) . 'build/style-index.css';
		if ( file_exists( $style_file ) ) {
			$style_dependencies = array( 'wp-components' );
			if ( wp_style_is( 'wordpress-backend-skill-fixture-tokens', 'registered' ) ) {
				$style_dependencies[] = 'wordpress-backend-skill-fixture-tokens';
			}
			wp_enqueue_style(
				'wordpress-backend-skill-fixture-style',
				plugins_url( 'build/style-index.css', __FILE__ ),
				$style_dependencies,
				$asset['version']
			);
			wp_style_add_data( 'wordpress-backend-skill-fixture-style', 'rtl', 'replace' );
		}
	}
);

function wbui_fixture_render_page() {
	$capability = is_network_admin() ? 'manage_network_options' : 'manage_options';
	$mode       = wbui_fixture_get_mode();
	$state      = wbui_fixture_get_state();
	$notice     = wbui_fixture_get_notice();

	if ( ! current_user_can( $capability ) ) {
		wp_die( esc_html__( 'You are not allowed to view this fixture.', 'wordpress-backend-skill-fixture' ) );
	}

	if ( 'success' === $notice ) {
		add_settings_error(
			'wbui_fixture_messages',
			'wbui_fixture_success',
			esc_html__( 'The fixture completed successfully.', 'wordpress-backend-skill-fixture' ),
			'success'
		);
	} elseif ( 'error' === $notice ) {
		add_settings_error(
			'wbui_fixture_messages',
			'wbui_fixture_error',
			esc_html__( 'The fixture could not complete its checks.', 'wordpress-backend-skill-fixture' ),
			'error'
		);
	} elseif ( 'partial' === $notice ) {
		add_settings_error(
			'wbui_fixture_messages',
			'wbui_fixture_partial',
			esc_html__( 'The fixture completed only part of its checks.', 'wordpress-backend-skill-fixture' ),
			'warning'
		);
	}
	?>
	<div class="wrap" data-wbui-mode="<?php echo esc_attr( $mode ); ?>" data-wbui-state="<?php echo esc_attr( $state ); ?>" data-wbui-notice="<?php echo esc_attr( $notice ); ?>">
		<h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
		<hr class="wp-header-end">

		<?php settings_errors( 'wbui_fixture_messages' ); ?>

		<div class="wbui-fixture-page-flow">
			<?php if ( ! is_network_admin() && in_array( $mode, array( 'classic', 'hybrid' ), true ) ) : ?>
				<form action="options.php" method="post">
					<?php
					settings_fields( 'wbui_fixture_settings' );
					do_settings_sections( WBUI_FIXTURE_SLUG );
					submit_button( esc_html__( 'Save settings', 'wordpress-backend-skill-fixture' ) );
					?>
				</form>
			<?php endif; ?>

			<?php if ( 'classic' !== $mode ) : ?>
				<?php if ( ! file_exists( plugin_dir_path( __FILE__ ) . 'build/index.asset.php' ) ) : ?>
					<div class="notice notice-error inline">
						<p><?php echo esc_html__( 'The fixture build is missing. Run the documented build command before testing this runtime.', 'wordpress-backend-skill-fixture' ); ?></p>
					</div>
				<?php else : ?>
					<div id="wbui-fixture-app"></div>
				<?php endif; ?>
			<?php endif; ?>
		</div>
	</div>
	<?php
}
