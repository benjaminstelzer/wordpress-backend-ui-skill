import {
	Button,
	Flex,
	FlexItem,
	Notice,
	TextControl,
} from '@wordpress/components';
import { dateI18n } from '@wordpress/date';
import { createRoot, lazy, Suspense, useState } from '@wordpress/element';
import { __ } from '@wordpress/i18n';
import './style.scss';

const WpdsStackRegion = lazy( () =>
	import( '@wordpress/ui' ).then( ( { Stack } ) => ( {
		default: function WpdsStackRegionComponent( { title, description } ) {
			return (
				<Stack className="wbui-fixture-wpds-stack" direction="column" gap="sm">
					<h2 id="wbui-wpds-title" className="wbui-fixture-flow-heading">
						{ title }
					</h2>
					<p className="wbui-fixture-flow-copy">{ description }</p>
				</Stack>
			);
		},
	} ) )
);

function HeadingBlock( { id, title, description } ) {
	return (
		<Flex
			className="wbui-fixture-heading-flow"
			direction="column"
			align="stretch"
			justify="flex-start"
			wrap={ false }
			expanded={ true }
			gap={ 2 }
		>
			<FlexItem>
				<h2 id={ id } className="wbui-fixture-flow-heading">
					{ title }
				</h2>
			</FlexItem>
			<FlexItem>
				<p className="wbui-fixture-flow-copy">{ description }</p>
			</FlexItem>
		</Flex>
	);
}

function WpdsLoadingRegion( { title } ) {
	return (
		<Flex
			className="wbui-fixture-heading-flow"
			data-wbui-wpds-fallback="true"
			direction="column"
			align="stretch"
			justify="flex-start"
			wrap={ false }
			expanded={ true }
			gap={ 2 }
		>
			<FlexItem>
				<h2 id="wbui-wpds-title" className="wbui-fixture-flow-heading">
					{ title }
				</h2>
			</FlexItem>
			<FlexItem>
				<span role="status">
					{ __( 'Loading the bundled WPDS region.', 'wordpress-backend-skill-fixture' ) }
				</span>
			</FlexItem>
		</Flex>
	);
}

function StateFeedback( { state, onReset } ) {
	if ( state === 'loading' ) {
		const message = __( 'Loading the fixture data.', 'wordpress-backend-skill-fixture' );

		return (
			<Notice status="info" isDismissible={ false } spokenMessage={ message }>
				<span id="wbui-loading-status">
					{ message }
				</span>
			</Notice>
		);
	}

	if ( state === 'partial' ) {
		const message = __( 'Some fixture results are available, but the accessibility checks are still missing.', 'wordpress-backend-skill-fixture' );

		return (
			<Notice
				status="warning"
				isDismissible={ false }
				spokenMessage={ message }
				actions={ [
					{
						label: __( 'Retry fixture checks', 'wordpress-backend-skill-fixture' ),
						variant: 'secondary',
						onClick: onReset,
					},
				] }
			>
				<p>{ message }</p>
			</Notice>
		);
	}

	if ( state === 'empty' ) {
		const message = __( 'No fixture result exists yet.', 'wordpress-backend-skill-fixture' );

		return (
			<Notice
				status="info"
				isDismissible={ false }
				spokenMessage={ message }
				actions={ [
					{
						label: __( 'Create example result', 'wordpress-backend-skill-fixture' ),
						variant: 'secondary',
						onClick: onReset,
					},
				] }
			>
				<p>{ message }</p>
			</Notice>
		);
	}

	if ( state === 'error' ) {
		const message = __( 'The fixture data could not be loaded.', 'wordpress-backend-skill-fixture' );

		return (
			<Notice
				status="error"
				isDismissible={ false }
				spokenMessage={ message }
				actions={ [
					{
						label: __( 'Retry fixture load', 'wordpress-backend-skill-fixture' ),
						variant: 'secondary',
						onClick: onReset,
					},
				] }
			>
				<p>{ message }</p>
			</Notice>
		);
	}

	if ( state === 'permission' ) {
		const message = __( 'This account cannot change the fixture value.', 'wordpress-backend-skill-fixture' );

		return (
			<Notice
				status="warning"
				isDismissible={ false }
				spokenMessage={ message }
				actions={ [
					{
						label: __( 'Return to the dashboard', 'wordpress-backend-skill-fixture' ),
						url: window.wbuiFixtureData?.dashboardUrl,
					},
				] }
			>
				<p id="wbui-permission-reason">{ message }</p>
			</Notice>
		);
	}

	return null;
}

function CoreWorkflow( { state, onStateChange } ) {
	const [ value, setValue ] = useState( '' );
	const successMessage = __( 'The test value was saved for this browser session.', 'wordpress-backend-skill-fixture' );
	const isUnavailable = [ 'loading', 'disabled', 'permission' ].includes( state );
	const help = state === 'disabled'
		? (
			<span id="wbui-disabled-reason" className="wbui-fixture-help-text">
				{ __( 'The value stays unavailable until the fixture prerequisites are complete.', 'wordpress-backend-skill-fixture' ) }
			</span>
		)
		: (
			<span className="wbui-fixture-help-text">
				{ __( 'Use a long value to test wrapping and vertical flow.', 'wordpress-backend-skill-fixture' ) }
			</span>
		);
	const disabledDescription = state === 'loading'
		? 'wbui-loading-status'
		: state === 'disabled'
			? 'wbui-disabled-reason'
			: state === 'permission'
				? 'wbui-permission-reason'
				: undefined;

	return (
		<section aria-labelledby="wbui-workflow-title">
			<Flex
				direction="column"
				align="stretch"
				justify="flex-start"
				wrap={ false }
				expanded={ true }
				gap={ 4 }
			>
				<FlexItem>
					<HeadingBlock
						id="wbui-workflow-title"
						title={ __( 'Core Components workflow', 'wordpress-backend-skill-fixture' ) }
						description={ __( 'Change one value and keep the result visible in the same task region.', 'wordpress-backend-skill-fixture' ) }
					/>
				</FlexItem>

				{ state === 'success' && (
					<FlexItem>
						<Notice
							status="success"
							isDismissible={ true }
							spokenMessage={ successMessage }
							onRemove={ () => onStateChange( 'initial' ) }
						>
							{ successMessage }
						</Notice>
					</FlexItem>
				) }

				{ ! [ 'initial', 'success', 'disabled' ].includes( state ) && (
					<FlexItem>
						<StateFeedback state={ state } onReset={ () => onStateChange( 'initial' ) } />
					</FlexItem>
				) }

				<FlexItem>
					<TextControl
						label={ __( 'Translated test value', 'wordpress-backend-skill-fixture' ) }
						help={ help }
						value={ value }
						onChange={ setValue }
						disabled={ isUnavailable }
						__next40pxDefaultSize
					/>
				</FlexItem>
				<FlexItem>
					<Flex
						className="wbui-fixture-action-row"
						direction="row"
						align="center"
						justify="flex-start"
						wrap={ true }
						expanded={ false }
						gap={ 2 }
					>
						<FlexItem>
							<Button
								variant="primary"
								onClick={ () => onStateChange( 'success' ) }
								disabled={ isUnavailable }
								accessibleWhenDisabled
								isBusy={ state === 'loading' }
								aria-describedby={ disabledDescription }
								__next40pxDefaultSize
							>
								{ __( 'Save test value', 'wordpress-backend-skill-fixture' ) }
							</Button>
						</FlexItem>
						<FlexItem>
							<Button
								variant="secondary"
								onClick={ () => setValue( '' ) }
								disabled={ isUnavailable }
								accessibleWhenDisabled
								aria-describedby={ disabledDescription }
								__next40pxDefaultSize
							>
								{ __( 'Reset test value', 'wordpress-backend-skill-fixture' ) }
							</Button>
						</FlexItem>
					</Flex>
				</FlexItem>
			</Flex>
		</section>
	);
}

function WpdsRegion() {
	const title = __( 'Bundled WPDS region', 'wordpress-backend-skill-fixture' );

	return (
		<section aria-labelledby="wbui-wpds-title">
			<Suspense fallback={ <WpdsLoadingRegion title={ title } /> }>
				<WpdsStackRegion
					title={ title }
					description={ __( 'This region uses the public Stack API and bundled WPDS design tokens.', 'wordpress-backend-skill-fixture' ) }
				/>
			</Suspense>
		</section>
	);
}

function DataView() {
	const fixtureData = window.wbuiFixtureData || {};

	return (
		<section aria-labelledby="wbui-data-view-title">
			<Flex
				direction="column"
				align="stretch"
				justify="flex-start"
				wrap={ false }
				expanded={ true }
				gap={ 4 }
			>
				<FlexItem>
					<HeadingBlock
						id="wbui-data-view-title"
						title={ __( 'Responsive data view', 'wordpress-backend-skill-fixture' ) }
						description={ __( 'The table scrolls locally when its columns cannot reflow.', 'wordpress-backend-skill-fixture' ) }
					/>
				</FlexItem>
				<FlexItem>
					<div
						className="wbui-fixture-data-scroll"
						tabIndex="0"
						role="region"
						aria-label={ __( 'Fixture result table', 'wordpress-backend-skill-fixture' ) }
					>
						<table className="widefat striped wbui-fixture-data-table">
							<thead>
								<tr>
									<th>{ __( 'Item', 'wordpress-backend-skill-fixture' ) }</th>
									<th>{ __( 'Localized number', 'wordpress-backend-skill-fixture' ) }</th>
									<th>{ __( 'Server-formatted date', 'wordpress-backend-skill-fixture' ) }</th>
									<th>{ __( 'JavaScript-formatted date', 'wordpress-backend-skill-fixture' ) }</th>
								</tr>
							</thead>
							<tbody>
								<tr>
									<td>{ __( 'Example item', 'wordpress-backend-skill-fixture' ) }</td>
									<td>{ fixtureData.formattedNumber }</td>
									<td>{ fixtureData.formattedDate }</td>
									<td>{ dateI18n( fixtureData.dateFormat, fixtureData.fixtureDateIso ) }</td>
								</tr>
							</tbody>
						</table>
					</div>
				</FlexItem>
			</Flex>
		</section>
	);
}

function FixtureApp() {
	const fixtureData = window.wbuiFixtureData || {};
	const mode = fixtureData.mode || 'hybrid';
	const [ state, setState ] = useState( fixtureData.state || 'initial' );
	const regions = [];

	if ( mode === 'core' || mode === 'hybrid' ) {
		regions.push( <CoreWorkflow key="core" state={ state } onStateChange={ setState } /> );
	}
	if ( mode === 'wpds' || mode === 'hybrid' ) {
		regions.push( <WpdsRegion key="wpds" /> );
	}
	if (
		( mode === 'core' || mode === 'hybrid' ) &&
		! [ 'empty', 'loading', 'error' ].includes( state )
	) {
		regions.push( <DataView key="data" /> );
	}

	return (
		<Flex
			className="wbui-fixture-root"
			direction="column"
			align="stretch"
			justify="flex-start"
			wrap={ false }
			expanded={ true }
			gap={ 8 }
		>
			{ regions.map( ( region ) => <FlexItem key={ region.key }>{ region }</FlexItem> ) }
		</Flex>
	);
}

const rootElement = document.getElementById( 'wbui-fixture-app' );

if ( rootElement ) {
	createRoot( rootElement ).render( <FixtureApp /> );
}
