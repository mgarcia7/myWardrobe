$.getJSON('/items_info', function(data) {
    $('.clothes').each(function() {

    	$(this).typeahead({
		    source: function (query, process) {
					items = [];
				    map = {};
				
				 
				    $.each(data, function (i, item) {
				        map[item.itemDesc] = item;
				        items.push(item.itemDesc);
				    });
				 
				    process(items);
		    },
		    updater: function (item) {
		        selectedItem = map[item].itemID;
    			return item;
		    },
			matcher: function (item) {
			    if (item.toLowerCase().indexOf(this.query.trim().toLowerCase()) != -1) {
			        return true;
			    }
			},
		    sorter: function (items) {
		        return items.sort();
		    },
		    highlighter: function (item) {
		        var regex = new RegExp( '(' + this.query + ')', 'gi' );
    			return item.replace( regex, "<strong>$1</strong>" );
		    },
		});
   	});

};