# Great Expectations - Data Validation
import great_expectations as gx
import great_expectations.expectations as gxe

# Logging 
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

def get_gx_context():
    """
    Retrieve the Great Expectations context.

    Returns:
        gx.DataContext: The Great Expectations context object.
    """
    logging.info("Retrieving Great Expectations context.")
    return gx.get_context()

def gx_validation(asset_name, suite_name, df, gx_expectations_object):
    logging.info(f"Starting validation for asset '{asset_name}' with suite '{suite_name}'.")
    # Connect data to GX
    gx_context = get_gx_context()
    
    try:
        data_source = gx_context.data_sources.add_pandas("pandas")
        logging.info("Added new pandas data source.")
    except gx.exceptions.DataContextError:
        data_source = gx_context.data_sources.get("pandas")
        logging.info("Retrieved existing pandas data source.")
    
    try:
        data_asset = data_source.add_dataframe_asset(name=asset_name)
        logging.info(f"Added data asset '{asset_name}'.")
    except gx.exceptions.DataContextError:
        data_asset = data_source.get_dataframe_asset(name=asset_name)
        logging.info(f"Retrieved existing data asset '{asset_name}'.")

    batch_definition_name = f"batch_definition_{asset_name}"
    try:    
        batch_definition = data_asset.get_batch_definition(name=batch_definition_name)
        logging.info(f"Retrieved batch definition '{batch_definition_name}'.")
    except KeyError:
        batch_definition = data_asset.add_batch_definition_whole_dataframe(name=batch_definition_name)
        logging.info(f"Added new batch definition '{batch_definition_name}'.")

    batch_parameters = {"dataframe": df}
    batch = batch_definition.get_batch(batch_parameters=batch_parameters)
    logging.info("Created batch for validation.")

    # Suites
    try:
        suite = gx_context.suites.add(gx.ExpectationSuite(name=suite_name))
        logging.info(f"Added new expectation suite '{suite_name}'.")
    except gx.exceptions.DataContextError:
        gx_context.suites.delete(name=suite_name)
        suite = gx_context.suites.add(gx.ExpectationSuite(name=suite_name))
        logging.info(f"Replaced existing expectation suite '{suite_name}'.")

    for expectation in gx_expectations_object:
        suite.add_expectation(expectation)
        logging.info(f"Added expectation '{expectation}'.")
    
    # Validate data
    logging.info("Beginning data validation.")
    validation_results = batch.validate(suite)
    logging.info("Data validation completed.")

    # Results checking
    if not validation_results["success"]:
        logging.error(f"Validation failed for {asset_name} with suite {suite_name}.")
        logging.error(validation_results)
        
        logging.info("Failed validation details:") 
        for result in validation_results["results"]:
            logging.error(result)  
    else:
        logging.info(f"Validation succeeded for {asset_name} with suite {suite_name}.")
        
        logging.info("Validation details:") 
        for result in validation_results["results"]:
            logging.info(result)
            
    return validation_results

def db_validation(df_gtd):
    gtd_expectations = [
        gxe.ExpectTableColumnsToMatchOrderedList(
            column_list=[
                'eventid', 'iyear', 'imonth', 'iday', 'extended', 'country_txt',
                'country', 'region_txt', 'region', 'city', 'latitude', 'longitude',
                'vicinity', 'crit1', 'crit2', 'crit3', 'doubtterr', 'multiple',
                'success', 'suicide', 'attacktype1_txt', 'attacktype1', 'targtype1_txt',
                'targtype1', 'natlty1_txt', 'natlty1', 'gname', 'guncertain1',
                'individual', 'nperps', 'nperpcap', 'claimed', 'weaptype1_txt',
                'weaptype1', 'nkill', 'nwound', 'property', 'ishostkid', 'INT_ANY',
                'date', 'date_country_actor'
                ]
            ),
        gxe.ExpectColumnValuesToBeBetween(column="iyear", min_value=1970, max_value=2017),
        gxe.ExpectColumnValuesToBeBetween(column="imonth", min_value=1, max_value=12),
        gxe.ExpectColumnValuesToBeBetween(column="iday", min_value=1, max_value=31),
        gxe.ExpectColumnValuesToBeBetween(column="country", min_value=4, max_value=1004),
        gxe.ExpectColumnValuesToBeBetween(column="region", min_value=1, max_value=12),
        gxe.ExpectColumnValuesToBeBetween(column="latitude", min_value=-42.250458, max_value=999.0),
        gxe.ExpectColumnValuesToBeBetween(column="longitude", min_value=-157.858333, max_value=179.366667),
        gxe.ExpectColumnValuesToBeBetween(column="attacktype1", min_value=1, max_value=9),
        gxe.ExpectColumnValuesToBeBetween(column="targtype1", min_value=1, max_value=22),
        gxe.ExpectColumnValuesToBeBetween(column="natlty1", min_value=4, max_value=1004),
        gxe.ExpectColumnValuesToBeBetween(column="nperps", min_value=0, max_value=25000),
        gxe.ExpectColumnValuesToBeBetween(column="nperpcap", min_value=0, max_value=999),
        gxe.ExpectColumnValuesToBeBetween(column="weaptype1", min_value=1, max_value=13),
        gxe.ExpectColumnValuesToBeBetween(column="nkill", min_value=0, max_value=1384),
        gxe.ExpectColumnValuesToBeBetween(column="nwound", min_value=0, max_value=8191),
        gxe.ExpectColumnValuesToBeInSet(column="extended", value_set=[0, 1]),
        gxe.ExpectColumnValuesToBeInSet(column="vicinity", value_set=[0, 1, 999]),
        gxe.ExpectColumnValuesToBeInSet(column="crit1", value_set=[1, 0]),
        gxe.ExpectColumnValuesToBeInSet(column="crit2", value_set=[1, 0]),
        gxe.ExpectColumnValuesToBeInSet(column="crit3", value_set=[1, 0]),
        gxe.ExpectColumnValuesToBeInSet(column="doubtterr", value_set=[0.0]),
        gxe.ExpectColumnValuesToBeInSet(column="multiple", value_set=[0.0, 1.0]),
        gxe.ExpectColumnValuesToBeInSet(column="success", value_set=[1, 0]),
        gxe.ExpectColumnValuesToBeInSet(column="suicide", value_set=[0, 1]),
        gxe.ExpectColumnValuesToBeInSet(column="guncertain1", value_set=[0.0, 1.0]),
        gxe.ExpectColumnValuesToBeInSet(column="individual", value_set=[0, 1]),
        gxe.ExpectColumnValuesToBeInSet(column="claimed", value_set=[0.0, 1.0, 999.0]),
        gxe.ExpectColumnValuesToBeInSet(column="property", value_set=[0, 1, 999]),
        gxe.ExpectColumnValuesToBeInSet(column="ishostkid", value_set=[0.0, 1.0, 999.0]),
        gxe.ExpectColumnValuesToBeInSet(column="INT_ANY", value_set=[999, 0, 1]),
        gxe.ExpectColumnValuesToNotBeNull(column="eventid"),
        gxe.ExpectColumnValuesToNotBeNull(column="iyear"),
        gxe.ExpectColumnValuesToNotBeNull(column="imonth"),
        gxe.ExpectColumnValuesToNotBeNull(column="iday"),
        gxe.ExpectColumnValuesToNotBeNull(column="extended"),
        gxe.ExpectColumnValuesToNotBeNull(column="country_txt"),
        gxe.ExpectColumnValuesToNotBeNull(column="country"),
        gxe.ExpectColumnValuesToNotBeNull(column="region_txt"),
        gxe.ExpectColumnValuesToNotBeNull(column="region"),
        gxe.ExpectColumnValuesToNotBeNull(column="city"),
        gxe.ExpectColumnValuesToNotBeNull(column="latitude"),
        gxe.ExpectColumnValuesToNotBeNull(column="longitude"),
        gxe.ExpectColumnValuesToNotBeNull(column="vicinity"),
        gxe.ExpectColumnValuesToNotBeNull(column="crit1"),
        gxe.ExpectColumnValuesToNotBeNull(column="crit2"),
        gxe.ExpectColumnValuesToNotBeNull(column="crit3"),
        gxe.ExpectColumnValuesToNotBeNull(column="doubtterr"),
        gxe.ExpectColumnValuesToNotBeNull(column="multiple"),
        gxe.ExpectColumnValuesToNotBeNull(column="success"),
        gxe.ExpectColumnValuesToNotBeNull(column="suicide"),
        gxe.ExpectColumnValuesToNotBeNull(column="attacktype1_txt"),
        gxe.ExpectColumnValuesToNotBeNull(column="attacktype1"),
        gxe.ExpectColumnValuesToNotBeNull(column="targtype1_txt"),
        gxe.ExpectColumnValuesToNotBeNull(column="targtype1"),
        gxe.ExpectColumnValuesToNotBeNull(column="natlty1_txt"),
        gxe.ExpectColumnValuesToNotBeNull(column="natlty1"),
        gxe.ExpectColumnValuesToNotBeNull(column="gname"),
        gxe.ExpectColumnValuesToNotBeNull(column="guncertain1"),
        gxe.ExpectColumnValuesToNotBeNull(column="individual"),
        gxe.ExpectColumnValuesToNotBeNull(column="nperps"),
        gxe.ExpectColumnValuesToNotBeNull(column="nperpcap"),
        gxe.ExpectColumnValuesToNotBeNull(column="claimed"),
        gxe.ExpectColumnValuesToNotBeNull(column="weaptype1_txt"),
        gxe.ExpectColumnValuesToNotBeNull(column="weaptype1"),
        gxe.ExpectColumnValuesToNotBeNull(column="nkill"),
        gxe.ExpectColumnValuesToNotBeNull(column="nwound"),
        gxe.ExpectColumnValuesToNotBeNull(column="property"),
        gxe.ExpectColumnValuesToNotBeNull(column="ishostkid"),
        gxe.ExpectColumnValuesToNotBeNull(column="INT_ANY"),
        gxe.ExpectColumnValuesToNotBeNull(column="date"),
        gxe.ExpectColumnValuesToNotBeNull(column="date_country_actor"),
        gxe.ExpectColumnValuesToBeOfType(column="eventid", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="iyear", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="imonth", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="iday", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="extended", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="country_txt", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="country", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="region_txt", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="region", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="city", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="latitude", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="longitude", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="vicinity", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="crit1", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="crit2", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="crit3", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="doubtterr", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="multiple", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="success", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="suicide", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="attacktype1_txt", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="attacktype1", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="targtype1_txt", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="targtype1", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="natlty1_txt", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="natlty1", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="gname", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="guncertain1", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="individual", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="nperps", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="nperpcap", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="claimed", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="weaptype1_txt", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="weaptype1", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="nkill", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="nwound", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="property", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="ishostkid", type_="float64"),
        gxe.ExpectColumnValuesToBeOfType(column="INT_ANY", type_="int64"),
        gxe.ExpectColumnValuesToBeOfType(column="date", type_="datetime64"),
        gxe.ExpectColumnValuesToBeOfType(column="date_country_actor", type_="str")
    ]
    
    return gx_validation("gtd", "gtd_suite", df_gtd, gtd_expectations)

def api_validation(df_api):
    api_exceptions = [
        gxe.ExpectTableColumnsToMatchOrderedList(
            column_list=[
                'event_date',
                'country',
                'disorder_type',
                'actor1'
                ]
        ),
        gxe.ExpectColumnValuesToNotBeNull(column="event_date"),
        gxe.ExpectColumnValuesToNotBeNull(column="country"),
        gxe.ExpectColumnValuesToNotBeNull(column="disorder_type"),
        gxe.ExpectColumnValuesToNotBeNull(column="actor1"),
        gxe.ExpectColumnValuesToBeOfType(column="event_date", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="country", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="disorder_type", type_="str"),
        gxe.ExpectColumnValuesToBeOfType(column="actor1", type_="str")
    ]
    
    return gx_validation("api", "api_suite", df_api, api_exceptions)