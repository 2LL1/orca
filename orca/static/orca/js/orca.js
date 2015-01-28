var orcaApp = angular.module('orcaApp', ['ngRoute', 'xeditable', 'ui.codemirror', 'ui.bootstrap', 'orcaControllers'])

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
    otherwise({redirectTo: '/home'});
}]);


Madlee.angular_config(orcaApp)

orcaApp.run(['editableOptions', function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
}]);

var orcaControllers = angular.module('orcaControllers', []);

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

    $http.post('/madlee/user/login', data).success(function(data) {
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

orcaControllers.controller('HomeCtrl', ['$scope', '$http', 
  function ($scope, $http) 
{
  Madlee.login_first()
  Madlee.active_navbar_tab('home')


}]);


var load_filter = function(data) {
  var filters = {text: 'Filters', icon: 'fa fa-filter', nodes: []}
    var status = {text: 'Status', icon: "fa fa-bars", nodes: [
        {
          id: 'D',
          text: "Developing",
          icon: "fa fa-steam"
        },
        {
          id: 'T',
          text: "Testing",
          icon: "fa fa-joomla"
        },
        {
          id: 'P',
          text: "Published",
          icon: "fa fa-rocket"
        },
        {
          id: 'X',
          text: "Deprecated",
          icon: "fa fa-recycle"
        }
      ]}
    var users =  {text: "User", icon: "fa fa-users", nodes: []}

    for (var i = 0; i < data.users.length; ++i) {
      users.nodes.push({text: data.users[i].username, icon: "fa fa-user"})
    }

    filters.nodes.push(status)
    filters.nodes.push(users)

    jQuery('#div-filter').treeview({data: [filters], levels: 3});
}
