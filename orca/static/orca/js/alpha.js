orcaControllers.controller('AlphaListCtrl', ['$scope', '$http', function ($scope, $http) {
  Madlee.login_first()
  Madlee.active_navbar_tab('alpha')

  $http.get('alpha.json').success(function(data){
    $scope.alphas = data
  })
  $http.get('alpha/filter').success(function(data){
    var filters = {text: 'Filters', icon: 'fa fa-filter', nodes: []}
    var status = {text: 'Status', icon: "fa fa-bars", nodes: [
        {
          text: "Developing",
          icon: "fa fa-steam"
        },
        {
          text: "Testing",
          icon: "fa fa-joomla"
        },
        {
          text: "Published",
          icon: "fa fa-rocket"
        },
        {
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
  })

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
      "window = 4\n" +
      "\n" +
      "close = ocean.get_frame('SDAY.close', date1, date2, window)\n" +
      "delta = close - pandas.rolling_mean(close, window+1)\n" +
      "\n" +
      "result = delta / close\n" +
      "result = result[window:]\n" +
      "\n"

    if ($routeParams.alphaID === 'new') {
      $scope.record = {
        id: null,
        name: "New Alpha",
        describe: "Say something here.",
        update_on: -1,
        status: 'D',
        update_code: $scope.DEFAULT_CODE,
        author: Madlee.user,
        owner: Madlee.user
      }
    }
    else {
      $http.get('alpha/'+ $routeParams.alphaID+ '.json').success(function(data) {
        $scope.record = data
      })
    }

    $scope.update_name = function() {
      if ($scope.record.id) {
        var data = {name: $scope.record.name};
        return $http.post('/orca/alpha/'+$scope.record.id+'/set_name', data);
      }
    };

    $scope.update_describe = function() {
      if ($scope.record.id) {
        var data = {describe: $scope.record.describe};
        return $http.post('/orca/alpha/'+$scope.record.id+'/set_describe', data);
      }
    };

    $scope.save = function() {
      var doc = $scope.editor.getDoc()
      $scope.record.update_code = doc.getValue()
      if ($scope.record.id === null) {
        $http.post('/orca/alpha/new', $scope.record).success(function(data) {
          window.location = '#/alpha-edit/' + data.id
        });
      }
      else {
        $http.post('/orca/alpha/'+$scope.record.id+'/save', $scope.record);
      }
    }



    $scope.codemirror_loaded = function(editor) {
      $scope.editor = editor
    }

    $scope.editor_options = {
      lineWrapping : true,
      lineNumbers: true,
      mode: 'python',
    }

}]);
