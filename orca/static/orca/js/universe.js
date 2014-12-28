orcaControllers.controller('UniverseListCtrl', ['$scope', 'Universe', 
	function ($scope, Universe) 
{
    Madlee.login_first()
    Madlee.active_navbar_tab('universe')
    
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

  $scope.universes = Universe.query()

}]);

orcaControllers.controller('UniverseDetailCtrl', ['$scope', '$routeParams', 'Universe', 
  function ($scope, $routeParams, Universe) {
    Madlee.login_first()
    Madlee.active_navbar_tab('universe')

    if ($routeParams.universeID === 'create') {
      $scope.universe = {
        id: null,
        name: "New Universe"
      }
    }
    else {
      $scope.universe = Universe.get({universeID: $routeParams.universeID}, function(universe) {
        
      });
    }

}]);
