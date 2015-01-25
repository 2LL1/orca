var pyxisApp = angular.module('pyxisApp', ['ngRoute', 'ui.bootstrap', 'pyxisControllers'])

pyxisApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
    when('/home', {templateUrl: 'home.html',   controller: 'HomeCtrl'}).
    when('/login', {templateUrl: 'login.html',   controller: 'LoginCtrl'}).
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
      if (is_undefined(v) || v === null) {
        return ''
      }
      else {
        return Madlee.timeshift(v)
      }
    }
});


pyxisControllers.controller('HomeCtrl', ['$scope', '$http', '$interval',
  function ($scope, $http, $interval) 
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
    $scope.current_cmd_id = id
    $scope.user_password = ''
    jQuery('#dlg-start-job').modal('show')
  }

  $scope.submit_job = function() {
    $scope.error_message = undefined
    $http.post('command/' + $scope.current_cmd_id + '/new_job', {password:$scope.user_password}).success(function(data) {
      if (data.status === 'success') {
        $scope.records.results.push(data)
        jQuery('#dlg-start-job').modal('hide')
      }
      else if (is_undefined(data.detail)) {
        $scope.error_message = "UNKNOW ERROR HAPPEND";
      }
      else {
        $scope.error_message = data.detail
      }
    })
  }

  $scope.refresh = function() {
    jQuery('.fa-refresh').addClass('fa-spin')
    $http.post('refresh').success(function(data) {
      jQuery('.fa-refresh').removeClass('fa-spin')
      if (data.status === 'success') {
        for (var i = 0; i < data.results.length; ++i) {
          for (var j = 0; j < $scope.records.results.length; ++j) {
            if (data.results[i].id === $scope.records.results[j].id) {
              $scope.records.results[j] = data.results[i]
            }
          }
        }
      }
      else if (is_undefined(data.detail)) {
        $scope.error_message = "UNKNOW ERROR HAPPEND";
      }
      else {
        $scope.error_message = data.detail
      }
    })

  }

  $interval($scope.refresh, 30000);

  $scope.load_page();

}]);
