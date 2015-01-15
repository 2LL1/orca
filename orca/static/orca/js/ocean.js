orcaControllers.controller('OceanListCtrl', ['$scope', 'Ocean', 
	function ($scope, Ocean) 
{
    Madlee.login_first()
    Madlee.active_navbar_tab('ocean')
    
    var filters = [{text: 'Filters', icon: 'fa fa-filter',
    nodes: [
    {
      text: "Status",
      icon: "fa fa-bars",
      nodes: [
        {
          text: "Ready",
          icon: "fa fa-star"
        },
        {
          text: "Preparing",
          icon: "fa fa-spin fa-spinner"
        },
        {
          text: "Closed",
          icon: "fa fa fa-graduation-cap"
        },
        {
          text: "Cancelled",
          icon: "fa fa-undo"
        }
      ]
    },
    {
      text: "User",
      icon: "fa fa-users",
      nodes: [
        {
          text: "madlee",
          icon: "fa fa-user"
        }
      ]
    },
    {
      text: "Created on", 
      icon: "fa fa-calendar",
      nodes: [
        {
          text: "Year",
          icon: "fa fa-calendar",
          nodes: [
            {
              text: "2014",
              icon: "fa fa-calendar"
            },
            {
              text: "2015",
              icon: "fa fa-calendar"
            }
          ]
        }
      ]
    }
  ]}]

  
  jQuery('#div-filter').treeview({data: filters, levels: 3});

  $scope.data = Ocean.query()

}]);

orcaControllers.controller('OceanDetailCtrl', ['$scope', '$routeParams', 'Ocean', 
  function ($scope, $routeParams, Ocean) {
    Madlee.login_first()
    Madlee.active_navbar_tab('ocean')

    $scope.data = Ocean.get({oceanID: $routeParams.oceanID}, function(record) {
      
    });

}]);


orcaControllers.controller('OceanEditCtrl', ['$scope', '$routeParams', 'Ocean', 
  function ($scope, $routeParams, Ocean) {
    Madlee.login_first()
    Madlee.active_navbar_tab('ocean')

    if ($routeParams.oceanID === 'create') {
      $scope.record = {
        id: null,
        name: "New Ocean"
      }
    }
    else {
      $scope.record = Ocean.get({oceanID: $routeParams.oceanID}, function(record) {
        
      });
    }

}]);
