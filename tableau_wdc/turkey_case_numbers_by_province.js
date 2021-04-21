(function () {
    var myConnector = tableau.makeConnector();

    myConnector.getSchema = function (schemaCallback) {
        var cols = [{
            id: "data_adi",
            alias: "province_name",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "data_detay",
            alias: "case_numbers_per_100k",
            dataType: tableau.dataTypeEnum.float
        }, {
            id: "original_week_period",
            description: "original week period",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "original_date_text",
            description: "original date of the data extracted from original_week_period",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "date",
            dataType: tableau.dataTypeEnum.date
        }];
    
        var tableSchema = {
            id: "turkeyCovid19ProvincialCaseNumbersFeed",
            alias: "Turkey case numbers per 100k by province",
            columns: cols,
            incrementColumnId: "date"
        };
    
        schemaCallback([tableSchema]);
    };

    myConnector.getData = function (table, doneCallback) {
        var lastDate = Date.parse(table.incrementValue) || new Date('2000-01-01'),
            dataArray = [];

        // Gather only the most recent data with an ID greater than 'lastDate'
        Papa.parse("https://github.com/jliew/tr-c19-provincial-case-numbers/raw/master/data/vaka_say%C4%B1s%C4%B1.csv", {
            header: true,
            download: true,
            skipEmptyLines: true,
            complete: function(results) {
                tableau.log("Using last date: " + lastDate)
                for (var i = 0, len = results.data.length; i < len; i++) {
                    row = results.data[i]
                    if (Date.parse(row.date) > lastDate) {
                        dataArray.push({
                            "data_adi": row.data_adi,
                            "data_detay": row.data_detay,
                            "original_week_period": row.original_week_period,
                            "original_date_text": row.original_date_text,
                            "date": row.date
                        });
                    }
                }

                table.appendRows(dataArray);
                doneCallback();
            }
        });

    };

    tableau.registerConnector(myConnector);

    $(document).ready(function () {
        $("#submitButton").click(function () {
            tableau.connectionName = "Turkey COVID-19 Provincial Case Numbers (per 100k) Feed";
            tableau.submit();
        });
    });
})();
