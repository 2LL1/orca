orcaControllers.controller('AdminCtrl', ['$scope', '$http', function ($scope, $http) {
	Madlee.login_first()
	Madlee.active_navbar_tab('admin')
}]);
