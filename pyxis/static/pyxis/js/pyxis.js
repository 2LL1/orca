var pyxisApp = angular.module('pyxisApp', ['ngRoute', 'ui.bootstrap', 'pyxisControllers'])

pyxisApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
    when('/home', {templateUrl: 'home.html',   controller: 'HomeCtrl'}).
    otherwise({redirectTo: '/home'});
}]);


Madlee.angular_config(pyxisApp)

var pyxisControllers = angular.module('pyxisControllers', []);

pyxisControllers.controller('LoginCtrl', ['$scope', '$http', function ($scope, $http) {
  if (is_undefined(Madlee.user)) {
    jQuery('.navbar').hide()
  }
  else {
    window.location = "#/home"
  }

  $scope.login = function() {
    var username = jQuery('#txt-username').val()
    var password = jQuery('#txt-password').val()
    var remember = jQuery('#chk_remember_me').attr("checked")

    data = {username: username, password: password, keep_login: remember}

    $http.post('/madlee/login.json', data).success(function(data) {
      window.location = '#/home'
    }).error(function() {

    })
  }
}]);


pyxisControllers.filter('timeshift',function(){
    return function(v) {
      if (is_undefined(v)) {
        return ''
      }
      else {
        return Madlee.timeshift(v)
      }
    }
});


pyxisControllers.controller('HomeCtrl', ['$scope', '$http', 
  function ($scope, $http) 
{
  Madlee.login_first()
  Madlee.active_navbar_tab('home')

  $scope.page_size=50
  $scope.records = {count: 0}
  $scope.current = 1

  $http.get('account').success(function(data) {
    $scope.accounts = data
  })

  $scope.load_page = function() {
    jQuery('.fa-refresh').addClass('fa-spin')
    $http.get('joblog').success(function(data){
      $scope.records = data
      jQuery('.fa-refresh').removeClass('fa-spin')
    })
  }

  $scope.start_jobs = function(id) {
    alert(id);
  }

  $scope.load_page();

}]);
