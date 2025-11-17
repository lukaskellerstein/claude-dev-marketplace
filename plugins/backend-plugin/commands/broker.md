---
description: Setup and configure message brokers (NATS, RabbitMQ, Redis, Kafka)
allowed-tools: Bash, Write, Read, Edit, Task
---

# Message Broker Command

Configure NATS, RabbitMQ, Redis Pub/Sub, or Kafka for event-driven architecture.

## Usage

`/broker [type] [action] [options]`

## Supported Brokers

- `nats` - NATS messaging system
- `rabbitmq` - RabbitMQ message broker
- `redis` - Redis Pub/Sub
- `kafka` - Apache Kafka

## Actions

- `setup` - Initial setup and configuration
- `connect` - Create connection module
- `publish` - Create publisher example
- `subscribe` - Create subscriber example
- `test` - Test connection

!`#!/bin/bash

BROKER=${1:-nats}
ACTION=${2:-setup}
OPTIONS=${3:-}

echo "🚀 Message Broker Configuration"
echo "📨 Broker: $BROKER"
echo "⚡ Action: $ACTION"

case $BROKER in
    nats)
        echo "Setting up NATS connection..."
        case $ACTION in
            setup)
                echo "Installing NATS dependencies..."
                if [ -f "package.json" ]; then
                    npm install nats
                elif [ -f "go.mod" ]; then
                    go get github.com/nats-io/nats.go
                elif [ -f "requirements.txt" ]; then
                    pip install nats-py
                fi
                echo "Please run: Task broker-specialist to complete NATS setup"
                ;;
            test)
                echo "Testing NATS connection..."
                echo "Please ensure NATS server is running: docker run -p 4222:4222 nats"
                ;;
            *)
                echo "Please run: Task broker-specialist for $ACTION implementation"
                ;;
        esac
        ;;
    rabbitmq)
        echo "Configuring RabbitMQ..."
        case $ACTION in
            setup)
                echo "Installing RabbitMQ dependencies..."
                if [ -f "package.json" ]; then
                    npm install amqplib
                elif [ -f "go.mod" ]; then
                    go get github.com/streadway/amqp
                elif [ -f "requirements.txt" ]; then
                    pip install aio-pika
                fi
                echo "Please run: Task broker-specialist to complete RabbitMQ setup"
                ;;
            test)
                echo "Testing RabbitMQ connection..."
                echo "Please ensure RabbitMQ is running: docker run -p 5672:5672 rabbitmq"
                ;;
            *)
                echo "Please run: Task broker-specialist for $ACTION implementation"
                ;;
        esac
        ;;
    redis)
        echo "Setting up Redis Pub/Sub..."
        case $ACTION in
            setup)
                echo "Installing Redis dependencies..."
                if [ -f "package.json" ]; then
                    npm install redis
                elif [ -f "go.mod" ]; then
                    go get github.com/go-redis/redis/v8
                elif [ -f "requirements.txt" ]; then
                    pip install aioredis
                fi
                echo "Please run: Task broker-specialist to complete Redis setup"
                ;;
            test)
                echo "Testing Redis connection..."
                echo "Please ensure Redis is running: docker run -p 6379:6379 redis"
                ;;
            *)
                echo "Please run: Task broker-specialist for $ACTION implementation"
                ;;
        esac
        ;;
    kafka)
        echo "Configuring Kafka..."
        case $ACTION in
            setup)
                echo "Installing Kafka dependencies..."
                if [ -f "package.json" ]; then
                    npm install kafkajs
                elif [ -f "go.mod" ]; then
                    go get github.com/Shopify/sarama
                elif [ -f "requirements.txt" ]; then
                    pip install aiokafka
                fi
                echo "Please run: Task broker-specialist to complete Kafka setup"
                ;;
            test)
                echo "Testing Kafka connection..."
                echo "Please ensure Kafka is running with docker-compose"
                ;;
            *)
                echo "Please run: Task broker-specialist for $ACTION implementation"
                ;;
        esac
        ;;
    *)
        echo "Unknown broker: $BROKER"
        echo "Supported brokers: nats, rabbitmq, redis, kafka"
        exit 1
        ;;
esac
`