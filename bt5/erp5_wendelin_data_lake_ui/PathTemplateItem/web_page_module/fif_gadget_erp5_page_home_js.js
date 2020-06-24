/*global window, rJS, RSVP, URI, document */
/*jslint nomen: true, indent: 2, maxerr: 3 */
(function (window, rJS, RSVP, document) {
  "use strict";
  /*function data_lake(context, evt) {
    var link = document.createElement('a');
    link.href = window.location.origin + "/erp5/web_site_module/fif_data_runner/#/?page=fifdata";
    link.click();
  }*/

  rJS(window)
    .declareAcquiredMethod("updateHeader", "updateHeader")
    .declareAcquiredMethod("getUrlForList", "getUrlForList")
    /*.declareJob('data_lake', function (evt) {
      return data_lake(this, evt);
    })*/
    .declareMethod("render", function (options) {
      return this.changeState(options);
    })
    .onStateChange(function () {
      var gadget = this;
      return gadget.updateHeader({
        page_title: 'Wendelin Data Lake Sharing Platform'
      })
        .push(function () {
          var url_parameter_list = [];
          url_parameter_list.push({
              command: 'display'
            });
          url_parameter_list.push({
              command: 'display_stored_state',
              options: {page: 'download'}
            });
          url_parameter_list.push({
              command: 'display_stored_state',
              options: {page: 'fifdata'}
            });
          url_parameter_list.push({
              command: 'display_stored_state',
              options: {page: 'register'}
            });
          url_parameter_list.push({
              command: 'display_stored_state',
              options: {page: 'ebulk_doc'}
            });
          return gadget.getUrlForList(url_parameter_list);
        })
        .push(function (url_list) {
          console.log("url_list:", url_list);
          console.log(document.querySelector("#register_link"));
        })
        .push(undefined, function (error) {
          throw error;
        });
    })
    /*.onEvent('submit', function (evt) {
      if (evt.target.name === 'data-lake') {
        return this.data_lake(evt);
      } else {
        throw new Error('Unknown form');
      }
    })*/;
}(window, rJS, RSVP, document));