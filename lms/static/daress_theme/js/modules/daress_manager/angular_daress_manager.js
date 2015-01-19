var daressManager = angular.module('daressManager', ['ui.router']);

daressManager.config(['$stateProvider', '$urlRouterProvider', '$urlMatcherFactoryProvider', function($stateProvider, $urlRouterProvider){
    
    $urlRouterProvider.otherwise('/');
    
    $stateProvider
        .state('home', {
            url: '/',
            templateUrl: 'payments.tmpl.html'
        })
    
        .state('users', {
            url: '/users',
            templateUrl: 'users.tmpl.html'
        })
    
        .state('payments', {
            url: '/payments',
            templateUrl: 'payments.tmpl.html',
            controller: 'payments'
        });
}]);

daressManager.controller('payments', function($scope) {
        $scope.submitChargeForm = function (chargeId) {
        console.log(chargeId);
        $('#'+chargeId+' form').submit();
    };
});