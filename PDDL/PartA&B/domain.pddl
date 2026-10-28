(define (domain lunar)
    (:requirements :strips :typing)
    
    ; -------------------------------
    ; Types
    ; -------------------------------

    ; EXAMPLE

    ; (:types
    ;     parent_type
    ;     child_type - parent_type

    ; )
    (:types
       lander - objects
       waypoint - objects
       rover - objects
    )

    ; -------------------------------
    ; Predicates
    ; -------------------------------

    ; EXAMPLE

    ; (:predicates
    ;     (no_arity_predicate)
    ;     (one_arity_predicate ?p - parameter_type)
    ; )

    (:predicates
        (connected ?w1 - waypoint ?w2 - waypoint)
        (at_lander ?l - lander ?w - waypoint)
        (at_rover ?r - rover ?w - waypoint)
        (deployed ?r - rover)
        (undeployed ?r - rover)
        (assigned ?r - rover ?l - lander)

        (has_image ?r - rover ?w - waypoint)
        (has_image_lander ?l - lander ?w - waypoint)
        (has_scan ?r - rover ?w - waypoint)
        (has_scan_lander ?l - lander ?w - waypoint)
        (has_storage ?r - rover)

        (has_sample_storage ?r - rover)
        (has_sample ?r - rover ?w - waypoint)
        (has_sample_lander ?l - lander ?w - waypoint)

    
    )

    ; -------------------------------
    ; Actions
    ; -------------------------------

    ; EXAMPLE

    ; (:action action-template
    ;     :parameters (?p - parameter_type)
    ;     :precondition (and
    ;         (one_arity_predicate ?p)
    ;     )
    ;     :effect 
    ;     (and 
    ;         (no_arity_predicate)
    ;         (not (one_arity_predicate ?p))
    ;     )
    ; )

    (:action deploy
        :parameters (?r - rover ?l - lander ?w - waypoint)
        :precondition (and
        (undeployed ?r)
        (assigned ?r ?l)
        (at_lander ?l ?w)
        )
        :effect (and
        (not (undeployed ?r))
        (deployed ?r)
        (at_rover ?r ?w)
        ) 
    )
    (:action Move
        :parameters (?r - rover ?w1 - waypoint ?w2 - waypoint)
        :precondition (and
        (deployed ?r)
        (at_rover ?r ?w1)
        (connected ?w1 ?w2))
        :effect (and
        (at_rover ?r ?w2)
        (not (at_rover ?r ?w1)))
        
    )    
    (:action Capture_image
        :parameters (?r - rover ?w - waypoint)
        :precondition (and
        (has_storage ?r)
        (at_rover ?r ?w)
        (deployed ?r)
        )
        :effect (and
        (not(has_storage ?r))
        (has_image ?r ?w))        
    )  

    (:action Capture_scan
        :parameters (?r - rover ?w - waypoint)
        :precondition (and
        (has_storage ?r)
        (at_rover ?r ?w)
        (deployed ?r)
        )
        :effect (and
        (not(has_storage ?r))
        (has_scan ?r ?w))        
    )

    (:action Transmit_image
        :parameters (?r - rover ?l - lander ?w - waypoint)
        :precondition (and
        (assigned ?r ?l)
        (has_image ?r ?w))
        :effect (and
        (not (has_image ?r ?w))
        (has_storage ?r)
        (has_image_lander ?l ?w))
        
    )    

    (:action Transmit_scan
        :parameters (?r - rover ?l - lander ?w - waypoint)
        :precondition (and
        (assigned ?r ?l)
        (has_scan ?r ?w))
        :effect (and
        (not (has_scan ?r ?w))
        (has_storage ?r)
        (has_scan_lander ?l ?w))
        
    ) 
    (:action Collect_sample
        :parameters (?r - rover ?w - waypoint)
        :precondition (and
        (deployed ?r)
        (at_rover ?r ?w)
        (has_sample_storage ?r))
        :effect (and
        (not(has_sample_storage ?r))
        (has_sample ?r ?w))
        
    )    
    (:action Return_sample
        :parameters (?r - rover ?l - lander ?w - waypoint ?w_sample - waypoint)
        :precondition (and
        (at_rover ?r ?w)
        (at_lander ?l ?w)
        (has_sample ?r ?w_sample)
        (deployed ?r)
        (assigned ?r ?l))
        :effect (and
        (not(has_sample ?r ?w_sample))
        (has_sample_storage ?r)
        (has_sample_lander ?l ?w_sample))
        
    )    


)