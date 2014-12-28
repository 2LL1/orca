orcaControllers.controller('AlphaListCtrl', ['$scope', 'Alpha', function ($scope, Alpha) {
    Madlee.login_first()
    Madlee.active_navbar_tab('alpha')
    
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

  $scope.alphas = Alpha.query()

}]);

orcaControllers.controller('AlphaDetailCtrl', ['$scope', '$routeParams', 'Alpha', 
  function ($scope, $routeParams, Alpha) {
    Madlee.login_first()
    Madlee.active_navbar_tab('alpha')

    if ($routeParams.alphaID === 'create') {
      $scope.alpha = {
        id: null,
        name: "New Alpha"
      }
    }
    else {
      $scope.alpha = Alpha.get({alphaID: $routeParams.alphaID}, function(alpha) {
        
      });
    }

    $scope.save = function() {
      if (is_undefined($scope.alpha)) {

      }
      else {
        Alpha.save($scope.alpha)
      }
    }

}]);
