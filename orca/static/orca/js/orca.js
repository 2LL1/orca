var orcaApp = angular.module('orcaApp', ['ngRoute', 'xeditable', 'ui.codemirror', 'orcaControllers', 'orcaServices'])

orcaApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
    when('/home', {templateUrl: 'home.html',   controller: 'HomeCtrl'}).
    when('/login', {templateUrl: 'login.html',   controller: 'LoginCtrl'}).
    when('/ocean', {templateUrl: 'ocean-list.html', controller: 'OceanListCtrl'}).
    when('/ocean-view/:oceanID', {templateUrl: 'ocean-view.html', controller: 'OceanDetailCtrl'}).
    when('/ocean-edit/:oceanID', {templateUrl: 'ocean-edit.html', controller: 'OceanEditCtrl'}).
    when('/alpha', {templateUrl: 'alpha-list.html', controller: 'AlphaListCtrl'}).
    when('/alpha-view/:alphaID', {templateUrl: 'alpha-view.html', controller: 'AlphaDetailCtrl'}).
    when('/alpha-edit/:alphaID', {templateUrl: 'alpha-edit.html', controller: 'AlphaEditCtrl'}).
    when('/universe', {templateUrl: 'universe-list.html', controller: 'UniverseListCtrl'}).
    when('/universe-view/:univID', {templateUrl: 'universe-view.html', controller: 'UniverseViewCtrl'}).
    when('/universe-edit/:univID', {templateUrl: 'universe-edit.html', controller: 'UniverseEditCtrl'}).
    
    when('/report', {templateUrl: 'report.html', controller: 'ReportCtrl'}).

    when('/admin', {templateUrl: 'admin.html', controller: 'AdminCtrl'}).
    otherwise({redirectTo: '/home'});
}]);


Madlee.angular_config(orcaApp)

orcaApp.run(['editableOptions', function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
}]);

var orcaControllers = angular.module('orcaControllers', []);

orcaServices = angular.module('orcaServices', ['ngResource'])

orcaServices.factory('Ocean', function($resource){
  return $resource('ocean/:oceanID.json', {}, {
    query: {method:'GET', params:{oceanID:''}, isArray:false},
  });
});


orcaServices.factory('Alpha', function($resource){
  return $resource('alpha/:alphaID.json', {}, {
    query: {method:'GET', params:{alphaID:''}, isArray:false},
  });
});

orcaServices.factory('Universe', function($resource){
  return $resource('universe/:universeID.json', {}, {
    query: {method:'GET', params:{universeID:''}, isArray:false},
  });
});


orcaControllers.controller('LoginCtrl', ['$scope', '$http', function ($scope, $http) {
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


orcaControllers.filter('timeshift',function(){
    return function(v) {
      if (is_undefined(v)) {
        return ''
      }
      else {
        return Madlee.timeshift(v)
      }
    }
});


orcaControllers.filter('prettify', ['$sce', function($sce){
    return function(text) {
        var result = prettyPrintOne(text);
        return  $sce.trustAsHtml(result)
    }
}])


orcaControllers.controller('HomeCtrl', ['$scope', '$http', 
  function ($scope, $http) 
{
  Madlee.login_first()
  Madlee.active_navbar_tab('home')


}]);
