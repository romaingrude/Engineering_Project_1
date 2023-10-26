<script>
    document.addEventListener("DOMContentLoaded", function () {
      var bookedDates = {{ booked_dates| tojson
    }};
    var unavailableDates = [];

    // Iterate over the booked dates and generate an array of unavailable dates
    bookedDates.forEach(function (dateRange) {
      var startDate = new Date(dateRange[0]);
      var endDate = new Date(dateRange[1]);

      for (var d = startDate; d <= endDate; d.setDate(d.getDate() + 1)) {
        unavailableDates.push(new Date(d));
      }
    });

    // Function to check if a date is in the unavailableDates array
    function isDateUnavailable(date) {
      return unavailableDates.some(function (unavailableDate) {
        return (
          date.getFullYear() === unavailableDate.getFullYear() &&
          date.getMonth() === unavailableDate.getMonth() &&
          date.getDate() === unavailableDate.getDate()
        );
      });
    }

    // Function to disable unavailable dates in the date inputs
    function disableUnavailableDates() {
      var startDateInput = document.getElementById("startdate");
      var endDateInput = document.getElementById("enddate");

      startDateInput.min = new Date().toISOString().split("T")[0];
      endDateInput.min = new Date().toISOString().split("T")[0];

      startDateInput.addEventListener("focus", function () {
        this.blur();
      });

      endDateInput.addEventListener("focus", function () {
        this.blur();
      });

      var dateInputs = document.querySelectorAll("input[type='date']");
      dateInputs.forEach(function (dateInput) {
        dateInput.addEventListener("click", function (event) {
          if (isDateUnavailable(new Date(this.value)) || new Date(this.value) < new Date()) {
            event.preventDefault();
          }
        });

        dateInput.addEventListener("mousedown", function (event) {
          event.preventDefault();
        });
      });
    }

    disableUnavailableDates();
    });
  </script>