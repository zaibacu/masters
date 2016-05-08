var demo = angular.module("demo", []);

demo.factory("SearchService", function($http){
	var service = {
		search: function(title){
			return $http.get("http://demo.dev/api/search/"+title);
		}
	};
	return service;
});

demo.controller("SearchCtrl", function($scope, SearchService){
	$scope.results = [];
	$scope.doSearch = function(title){
		SearchService.search(title).then(function(result){
			$scope.results = result.data;
		});
	};
});