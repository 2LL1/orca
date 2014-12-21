var orcaApp = angular.module('orcaApp', ['ngRoute', 'orcaControllers'])

orcaApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
    when('/home', {templateUrl: 'home.html',   controller: 'HomeCtrl'}).
    when('/login', {templateUrl: 'login.html',   controller: 'LoginCtrl'}).
    when('/alpha', {templateUrl: 'alpha-list.html', controller: 'AlphaListCtrl'}).
    when('/alpha/:alphaID', {templateUrl: 'alpha.html', controller: 'AlphaDetailCtrl'}).
    when('/universe', {templateUrl: 'universe-list.html', controller: 'UniverseListCtrl'}).
    when('/universe/:univID', {templateUrl: 'universe.html', controller: 'UniverseDetailCtrl'}).
    when('/category', {templateUrl: 'category-list.html', controller: 'CategoryListCtrl'}).
    when('/category/:catID', {templateUrl: 'category.html', controller: 'CategoryDetailCtrl'}).
    when('/admin', {templateUrl: 'admin.html', controller: 'AdminCtrl'}).
    otherwise({redirectTo: '/home'});
}]);


Madlee.angular_config(orcaApp)

var orcaControllers = angular.module('orcaControllers', []);

orcaControllers.controller('HomeCtrl', ['$scope', '$http', function ($scope, $http) {
	Madlee.login_first()
  Madlee.active_navbar_tab('home')
}]);

orcaControllers.controller('LoginCtrl', ['$scope', '$http', function ($scope, $http) {
  if (is_undefined(Madlee.user)) {
    jQuery('.navbar').hide()
  }
  else {
    window.location = "#/home"
  }

  $scope.login = function() {
    var username = jQuery('#inputEmail').val()
    var password = jQuery('#inputPassword').val()
    var remember = jQuery('#chk_remember_me').attr("checked")

    data = {email: username, password: password, keep_login: remember}

    $http.post('/madlee/login.json', data).success(function(data) {
      window.location = '#/home'
      
    }).error(function() {

    })
    
  }
}]);

