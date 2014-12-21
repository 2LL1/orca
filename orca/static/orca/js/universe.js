orcaControllers.controller('UniverseListCtrl', ['$scope', '$http', function ($scope, $http) {
	Madlee.login_first()
	Madlee.active_navbar_tab('universe')
	
}]);

orcaControllers.controller('UniverseDetailCtrl', ['$scope', '$http', function ($scope, $http) {
	Madlee.login_first()
	Madlee.active_navbar_tab('universe')
  
}]);
