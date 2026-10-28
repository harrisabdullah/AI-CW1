(define (problem lunar-mission-2)
    (:domain lunar)

    (:objects
        lander1 lander2 - lander
        rover1 rover2 - rover
        wp1 wp2 wp3 wp4 wp5 wp6 - waypoint
    )

    (:init
        (undeployed rover2)
        (deployed rover1)
        (at_lander lander1 wp2)
        (at_lander lander2 wp5)
        (at_rover rover1 wp2)
        (has_sample_storage rover1)
        (has_storage rover1)
        (has_sample_storage rover2)
        (has_storage rover2)
        (assigned rover1 lander1)
        (assigned rover2 lander2)

        (connected wp1 wp2)
        (connected wp2 wp3)
        (connected wp3 wp5)
        (connected wp2 wp1)
        (connected wp4 wp2)
        (connected wp5 wp3)
        (connected wp5 wp6)
        (connected wp6 wp4)
        (connected wp2 wp4)
    )

    (:goal
        (and
            (has_image_lander lander1 wp3)

            (has_scan_lander lander2 wp4)

            (has_image_lander lander2 wp2)

            (has_scan_lander lander1 wp6)

            (has_sample_lander lander1 wp5)

            (has_sample_lander lander2 wp1)
        )
    )
)