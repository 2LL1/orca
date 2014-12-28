orcaControllers.controller('CategoryListCtrl', ['$scope', 'Category', function ($scope, Category) {
    Madlee.login_first()
    Madlee.active_navbar_tab('category')
    
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

  $scope.categories = Category.query()

}]);

orcaControllers.controller('CategoryDetailCtrl', ['$scope', '$routeParams', 'Category', 
  function ($scope, $routeParams, Category) {
    Madlee.login_first()
    Madlee.active_navbar_tab('category')

    if ($routeParams.categoryID === 'create') {
      $scope.category = {
        id: null,
        name: "New Category"
      }
    }
    else {
      $scope.category = Category.get({categoryID: $routeParams.categoryID}, function(category) {
        
      });
    }

}]);
