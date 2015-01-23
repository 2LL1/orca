orcaControllers.controller('OceanListCtrl', ['$scope', '$http', function ($scope, $http) {
  Madlee.login_first()
  Madlee.active_navbar_tab('ocean')
    
  $scope.page_size=50
  $scope.records = {count: 0}
  $scope.current = 1

  $scope.load_page = function() {
    $http.get('ocean.json').success(function(data){
      $scope.records = data
    })
  }
  
  $http.get('ocean/filter').success(function(data){
    load_filter(data)
  })
  $scope.load_page();

}]);

orcaControllers.controller('OceanDetailCtrl', ['$scope', '$routeParams', '$http', 
  function ($scope, $routeParams, $http) {
    Madlee.login_first()
    Madlee.active_navbar_tab('ocean')

    

}]);



orcaControllers.controller('OceanEditCtrl', ['$scope', '$routeParams', '$http', 
  function ($scope, $routeParams, $http) {
    Madlee.login_first()
    Madlee.active_navbar_tab('ocean')

    $scope.DEFAULT_CODE = "# Define your code here.\n"
      + "# self is the ocean itself\n"
      + "self.refresh('username/password@hosts')\n"

    if ($routeParams.oceanID === 'new') {
      $scope.record = {
        id: null,
        name: "New Ocean",
        describe: "Say something here.",
        update_on: -1,
        status: 'D',
        update_code: $scope.DEFAULT_CODE,
        author: Madlee.user,
        owner: Madlee.user
      }
    }
    else {
      $http.get('ocean/'+ $routeParams.oceanID+ '.json').success(function(data) {
        $scope.record = data
      })
    }

    $scope.update_name = function() {
      if ($scope.record.id) {
        var data = {name: $scope.record.name};
        return $http.post('/orca/ocean/'+$scope.record.id+'/set_name', data);
      }
    };

    $scope.update_describe = function() {
      if ($scope.record.id) {
        var data = {describe: $scope.record.describe};
        return $http.post('/orca/ocean/'+$scope.record.id+'/set_describe', data);
      }
    };

    $scope.save = function() {
      var doc = $scope.editor.getDoc()
      $scope.record.update_code = doc.getValue()
      if ($scope.record.id === null) {
        $http.post('/orca/ocean/new', $scope.record).success(function(data) {
          window.location = '#/ocean-edit/' + data.id
        });
      }
      else {
        $http.post('/orca/ocean/'+$scope.record.id+'/save', $scope.record);
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
