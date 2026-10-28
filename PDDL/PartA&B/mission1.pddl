(define (problem lunar-mission-1)
    (:domain lunar)

    (:objects
    ;object naming
        rover1 - rover
        lander1 - lander
        wp1 wp2 wp3 wp4 wp5 - waypoint
    )

    (:init
        ;setup
        (undeployed rover1)
        (assigned rover1 lander1)
        (has_sample_storage rover1)
        (has_storage rover1)
        (at_lander lander1 wp2)
        (has_sample_lander_storage lander1)

        ;connecting waypoints
        (connected wp1 wp2)
        (connected wp1 wp4)
        (connected wp2 wp3)
        (connected wp3 wp5)
        (connected wp5 wp1)
        (connected wp4 wp3)

    )

    (:goal
        (and
            ;desired goals
           (has_image_lander lander1 wp5)

           (has_scan_lander lander1 wp3)

           (has_sample_lander lander1 wp1)


        )
    )
)