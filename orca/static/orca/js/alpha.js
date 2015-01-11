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

    $scope.data_loaded = false

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

    

    jQuery('#tab-alpha a').click(function (e) {
      e.preventDefault()
      jQuery(this).tab('show')
      $scope.data_loaded = true
    });

}]);



orcaControllers.controller('AlphaEditCtrl', ['$scope', '$routeParams', '$http', 
  function ($scope, $routeParams, $http) {
    Madlee.login_first()
    Madlee.active_navbar_tab('alpha')

    $scope.DEFAULT_CODE = "# Define your code here.\n" +
      "# This is an example.\n" +
      "# [date1, date2) are a pair of date.\n" +
      "# Save your output into variable result\n" +
      "\n" +
      "from orca import ocean\n" +
      "import pandas\n" +
      "import numpy\n" +
      "\n" +
      "window = 5\n" +
      "\n" +
      "close = ocean.get_frame('KDay.close', date1, date2, window)\n" +
      "delta = close - pandas.rolling_mean(close, window)\n" +
      "\n" +
      "result = delta / close\n" +
      "result = result[window:]\n" +
      "\n"

    $scope.data_loaded = false

    if ($routeParams.alphaID === 'new') {
      $scope.record = {
        id: null,
        name: "New Alpha",
        describe: "Say something here.",
        update_on: 'N/A',
        status: 'D',
        update_code: $scope.DEFAULT_CODE,
        author: Madlee.user,
        owner: Madlee.user
        // timestamp0: moment().format('YYYY-MM-DD HH:mm:ss')
      }
    }
    else {
      
    }

    $scope.save = function() {
      $routeParams.alphaID = 'HELLO'

      // $http.post('alpha/'+ $routeParams.alphaID+ '.json', {data: $scope.record})
    }

    $scope.editor_options = {
      lineWrapping : true,
      lineNumbers: true,
      mode: 'python'
    }

}]);
