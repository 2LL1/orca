orcaControllers.controller('CategoryListCtrl', ['$scope', '$http', function ($scope, $http) {
	Madlee.login_first()
	Madlee.active_navbar_tab('category')
	
}]);

orcaControllers.controller('CategoryDetailCtrl', ['$scope', '$http', function ($scope, $http) {
	Madlee.login_first()
	Madlee.active_navbar_tab('category')
}]);
